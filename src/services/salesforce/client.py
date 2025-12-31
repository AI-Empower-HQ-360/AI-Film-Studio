"""Salesforce API client wrapper"""
import logging
from typing import Optional, Dict, Any
from simple_salesforce import Salesforce, SalesforceAuthenticationFailed
from src.config import settings

logger = logging.getLogger(__name__)


class SalesforceClient:
    """Wrapper for Salesforce API client with authentication and connection management"""
    
    def __init__(self):
        self._client: Optional[Salesforce] = None
        self._connected = False
    
    def connect(self) -> bool:
        """
        Establish connection to Salesforce using credentials from settings.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        if not settings.SALESFORCE_SYNC_ENABLED:
            logger.info("Salesforce sync is disabled")
            return False
        
        try:
            self._client = Salesforce(
                username=settings.SALESFORCE_USERNAME,
                password=settings.SALESFORCE_PASSWORD,
                security_token=settings.SALESFORCE_SECURITY_TOKEN,
                domain=settings.SALESFORCE_DOMAIN,
                version=settings.SALESFORCE_API_VERSION
            )
            self._connected = True
            logger.info(f"Successfully connected to Salesforce as {settings.SALESFORCE_USERNAME}")
            return True
        except SalesforceAuthenticationFailed as e:
            logger.error(f"Salesforce authentication failed: {e}")
            self._connected = False
            return False
        except Exception as e:
            logger.error(f"Failed to connect to Salesforce: {e}")
            self._connected = False
            return False
    
    def is_connected(self) -> bool:
        """Check if client is connected to Salesforce"""
        return self._connected and self._client is not None
    
    def get_client(self) -> Optional[Salesforce]:
        """
        Get the Salesforce client instance.
        
        Returns:
            Salesforce client if connected, None otherwise
        """
        if not self.is_connected():
            self.connect()
        return self._client
    
    def create_record(self, sobject_type: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Create a new record in Salesforce.
        
        Args:
            sobject_type: Salesforce object type (e.g., 'Contact', 'AI_Project__c')
            data: Record data as dictionary
        
        Returns:
            Record ID if successful, None otherwise
        """
        client = self.get_client()
        if not client:
            logger.error("Cannot create record: Not connected to Salesforce")
            return None
        
        try:
            result = getattr(client, sobject_type).create(data)
            if result.get('success'):
                record_id = result.get('id')
                logger.info(f"Created {sobject_type} record: {record_id}")
                return record_id
            else:
                logger.error(f"Failed to create {sobject_type}: {result.get('errors')}")
                return None
        except Exception as e:
            logger.error(f"Error creating {sobject_type} record: {e}")
            return None
    
    def update_record(self, sobject_type: str, record_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing record in Salesforce.
        
        Args:
            sobject_type: Salesforce object type
            record_id: Salesforce record ID
            data: Updated data as dictionary
        
        Returns:
            True if successful, False otherwise
        """
        client = self.get_client()
        if not client:
            logger.error("Cannot update record: Not connected to Salesforce")
            return False
        
        try:
            result = getattr(client, sobject_type).update(record_id, data)
            # Update returns 204 No Content on success
            logger.info(f"Updated {sobject_type} record: {record_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating {sobject_type} record {record_id}: {e}")
            return False
    
    def get_record(self, sobject_type: str, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a record from Salesforce.
        
        Args:
            sobject_type: Salesforce object type
            record_id: Salesforce record ID
        
        Returns:
            Record data as dictionary if found, None otherwise
        """
        client = self.get_client()
        if not client:
            logger.error("Cannot get record: Not connected to Salesforce")
            return None
        
        try:
            record = getattr(client, sobject_type).get(record_id)
            return record
        except Exception as e:
            logger.error(f"Error retrieving {sobject_type} record {record_id}: {e}")
            return None
    
    def query(self, soql: str) -> Optional[Dict[str, Any]]:
        """
        Execute a SOQL query.
        
        Args:
            soql: SOQL query string
        
        Returns:
            Query results as dictionary if successful, None otherwise
        """
        client = self.get_client()
        if not client:
            logger.error("Cannot execute query: Not connected to Salesforce")
            return None
        
        try:
            results = client.query(soql)
            return results
        except Exception as e:
            logger.error(f"Error executing SOQL query: {e}")
            return None
    
    def find_by_external_id(self, sobject_type: str, external_id_field: str, external_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a record by external ID field.
        
        Args:
            sobject_type: Salesforce object type
            external_id_field: Name of the external ID field
            external_id: External ID value to search for
        
        Returns:
            Record data if found, None otherwise
        """
        soql = f"SELECT Id FROM {sobject_type} WHERE {external_id_field} = '{external_id}' LIMIT 1"
        results = self.query(soql)
        
        if results and results.get('totalSize', 0) > 0:
            return results['records'][0]
        return None
    
    def upsert_record(self, sobject_type: str, external_id_field: str, external_id: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Upsert (insert or update) a record using external ID.
        
        Args:
            sobject_type: Salesforce object type
            external_id_field: Name of the external ID field
            external_id: External ID value
            data: Record data
        
        Returns:
            Record ID if successful, None otherwise
        """
        client = self.get_client()
        if not client:
            logger.error("Cannot upsert record: Not connected to Salesforce")
            return None
        
        try:
            # Salesforce upsert uses external ID in URL
            result = getattr(client, sobject_type).upsert(
                f"{external_id_field}/{external_id}",
                data
            )
            
            # Upsert returns 201 for created or 204 for updated
            if isinstance(result, dict) and result.get('success'):
                record_id = result.get('id')
                logger.info(f"Upserted {sobject_type} record: {record_id}")
                return record_id
            else:
                # For updates, result might be 204 with no body
                logger.info(f"Upserted {sobject_type} with external ID: {external_id}")
                # Try to find the record to get its ID
                record = self.find_by_external_id(sobject_type, external_id_field, external_id)
                return record.get('Id') if record else None
        except Exception as e:
            logger.error(f"Error upserting {sobject_type} record: {e}")
            return None
