"use client";

/**
 * @label Image Creation Page
 * @description Next.js page for comprehensive image generation with all age groups, genders, cultures, animals, locations, and dress types
 */

import { useState, useEffect } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../components/ui/tabs";
import { Loader2, CheckCircle2, XCircle, Image as ImageIcon, Download } from "lucide-react";

interface Option {
  value: string;
  label: string;
  description?: string;
}

export default function ImageCreationPage() {
  const [prompt, setPrompt] = useState("");
  const [ageGroup, setAgeGroup] = useState<string>("");
  const [gender, setGender] = useState<string>("");
  const [culturalRegion, setCulturalRegion] = useState<string>("");
  const [bodyType, setBodyType] = useState<string>("");
  const [dressType, setDressType] = useState<string>("");
  const [location, setLocation] = useState<string>("");
  const [animalType, setAnimalType] = useState<string>("");
  const [style, setStyle] = useState("realistic");
  const [resolution, setResolution] = useState("1024x1024");
  const [numImages, setNumImages] = useState(1);
  const [negativePrompt, setNegativePrompt] = useState("");
  
  // Options data
  const [ageGroups, setAgeGroups] = useState<Option[]>([]);
  const [genders, setGenders] = useState<Option[]>([]);
  const [cultures, setCultures] = useState<Option[]>([]);
  const [animals, setAnimals] = useState<Option[]>([]);
  const [bodyTypes, setBodyTypes] = useState<Option[]>([]);
  const [dressTypes, setDressTypes] = useState<Option[]>([]);
  const [locations, setLocations] = useState<Option[]>([]);
  
  const [loading, setLoading] = useState(false);
  const [loadingOptions, setLoadingOptions] = useState(false);
  const [jobId, setJobId] = useState<string | null>(null);
  const [jobStatus, setJobStatus] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{
    images?: Array<{ image_id: string; url: string; metadata?: any }>;
    prompt?: string;
    processing_time?: number;
  } | null>(null);

  useEffect(() => {
    loadOptions();
  }, []);

  const loadOptions = async () => {
    setLoadingOptions(true);
    try {
      const [
        ageGroupsRes,
        gendersRes,
        culturesRes,
        animalsRes,
        bodyTypesRes,
        dressTypesRes,
        locationsRes
      ] = await Promise.all([
        api.request<{ age_groups: Option[] }>("/api/v1/images/options/age-groups"),
        api.request<{ genders: Option[] }>("/api/v1/images/options/genders"),
        api.request<{ cultures: Option[] }>("/api/v1/images/options/cultures"),
        api.request<{ animals: Option[] }>("/api/v1/images/options/animals"),
        api.request<{ body_types: Option[] }>("/api/v1/images/options/body-types"),
        api.request<{ dress_types: Option[] }>("/api/v1/images/options/dress-types"),
        api.request<{ locations: Option[] }>("/api/v1/images/options/locations")
      ]);
      
      setAgeGroups(ageGroupsRes.age_groups || []);
      setGenders(gendersRes.genders || []);
      setCultures(culturesRes.cultures || []);
      setAnimals(animalsRes.animals || []);
      setBodyTypes(bodyTypesRes.body_types || []);
      setDressTypes(dressTypesRes.dress_types || []);
      setLocations(locationsRes.locations || []);
    } catch (err) {
      console.error("Failed to load options:", err);
    } finally {
      setLoadingOptions(false);
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError("Please enter an image description");
      return;
    }

    setError(null);
    setLoading(true);
    setJobId(null);
    setJobStatus(null);
    setResult(null);

    try {
      const requestBody: any = {
        prompt,
        style,
        resolution,
        num_images: numImages
      };

      if (ageGroup) requestBody.age_group = ageGroup;
      if (gender) requestBody.gender = gender;
      if (culturalRegion) requestBody.cultural_region = culturalRegion;
      if (bodyType) requestBody.body_type = bodyType;
      if (dressType) requestBody.dress_type = dressType;
      if (location) requestBody.location = location;
      if (animalType) requestBody.animal_type = animalType;
      if (negativePrompt) requestBody.negative_prompt = negativePrompt;

      const response = await api.request<{ job_id: string; status: string }>(
        "/api/v1/images/generate",
        {
          method: "POST",
          body: JSON.stringify(requestBody)
        }
      );

      setJobId(response.job_id);
      setJobStatus(response.status);
      pollJobStatus(response.job_id);
    } catch (err: any) {
      setError(err.message || "Failed to start image generation");
      setLoading(false);
    }
  };

  const pollJobStatus = async (id: string) => {
    const maxAttempts = 60;
    let attempts = 0;

    const checkStatus = async () => {
      try {
        const status = await api.request<{
          job_id: string;
          status: string;
          images?: Array<{ image_id: string; url: string; metadata?: any }>;
          prompt?: string;
          processing_time?: number;
          error_message?: string;
        }>(`/api/v1/images/status/${id}`);

        setJobStatus(status.status);

        if (status.status === "completed") {
          setResult({
            images: status.images,
            prompt: status.prompt,
            processing_time: status.processing_time
          });
          setLoading(false);
        } else if (status.status === "failed") {
          setError(status.error_message || "Image generation failed");
          setLoading(false);
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(checkStatus, 5000);
        } else {
          setError("Job timeout - please check status manually");
          setLoading(false);
        }
      } catch (err: any) {
        setError(err.message || "Failed to check job status");
        setLoading(false);
      }
    };

    checkStatus();
  };

  return (
    <div className="container mx-auto py-8 px-4 max-w-7xl">
      <div className="mb-8">
        <h1 className="text-4xl font-bold mb-2">Image Creation Engine</h1>
        <p className="text-muted-foreground">
          Generate images for all age groups, genders, cultures, animals, locations, and dress types
        </p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-destructive/10 border border-destructive rounded-lg">
          <p className="text-destructive">{error}</p>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left Column - Configuration */}
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Image Description</CardTitle>
              <CardDescription>Describe what you want to generate</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="prompt">Image Description *</Label>
                <Textarea
                  id="prompt"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="e.g., A child playing flute by the ocean, A woman in traditional attire at a temple..."
                  rows={4}
                />
              </div>

              <div>
                <Label htmlFor="negative_prompt">Negative Prompt (Things to Avoid)</Label>
                <Textarea
                  id="negative_prompt"
                  value={negativePrompt}
                  onChange={(e) => setNegativePrompt(e.target.value)}
                  placeholder="e.g., blurry, low quality, distorted..."
                  rows={2}
                />
              </div>
            </CardContent>
          </Card>

          <Tabs defaultValue="people" className="space-y-4">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="people">
                <ImageIcon className="mr-2 h-4 w-4" />
                People
              </TabsTrigger>
              <TabsTrigger value="animals">
                <ImageIcon className="mr-2 h-4 w-4" />
                Animals
              </TabsTrigger>
            </TabsList>

            <TabsContent value="people" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>People Attributes</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="age_group">Age Group</Label>
                      <Select value={ageGroup} onValueChange={setAgeGroup}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select age group" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="">None</SelectItem>
                          {ageGroups.map((ag) => (
                            <SelectItem key={ag.value} value={ag.value}>
                              {ag.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="gender">Gender</Label>
                      <Select value={gender} onValueChange={setGender}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select gender" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="">None</SelectItem>
                          {genders.map((g) => (
                            <SelectItem key={g.value} value={g.value}>
                              {g.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="cultural_region">Cultural Region</Label>
                    <Select value={culturalRegion} onValueChange={setCulturalRegion}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select cultural region" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">None</SelectItem>
                        {cultures.map((c) => (
                          <SelectItem key={c.value} value={c.value}>
                            {c.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="body_type">Body Type</Label>
                      <Select value={bodyType} onValueChange={setBodyType}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select body type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="">None</SelectItem>
                          {bodyTypes.map((bt) => (
                            <SelectItem key={bt.value} value={bt.value}>
                              {bt.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="dress_type">Dress Type</Label>
                      <Select value={dressType} onValueChange={setDressType}>
                        <SelectTrigger>
                          <SelectValue placeholder="Select dress type" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="">None</SelectItem>
                          {dressTypes.map((dt) => (
                            <SelectItem key={dt.value} value={dt.value}>
                              {dt.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="location">Location/Setting</Label>
                    <Select value={location} onValueChange={setLocation}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select location" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">None</SelectItem>
                        {locations.map((loc) => (
                          <SelectItem key={loc.value} value={loc.value}>
                            {loc.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="animals" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Animal Attributes</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="animal_type">Animal Type</Label>
                    <Select value={animalType} onValueChange={setAnimalType}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select animal type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">None</SelectItem>
                        {animals.map((animal) => (
                          <SelectItem key={animal.value} value={animal.value}>
                            {animal.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="animal_location">Location/Setting</Label>
                    <Select value={location} onValueChange={setLocation}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select location" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">None</SelectItem>
                        {locations.map((loc) => (
                          <SelectItem key={loc.value} value={loc.value}>
                            {loc.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          <Card>
            <CardHeader>
              <CardTitle>Generation Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="style">Style</Label>
                  <Select value={style} onValueChange={setStyle}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="realistic">Realistic</SelectItem>
                      <SelectItem value="artistic">Artistic</SelectItem>
                      <SelectItem value="cinematic">Cinematic</SelectItem>
                      <SelectItem value="traditional">Traditional</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="resolution">Resolution</Label>
                  <Select value={resolution} onValueChange={setResolution}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1024x1024">1024x1024 (Square)</SelectItem>
                      <SelectItem value="1024x768">1024x768 (Landscape)</SelectItem>
                      <SelectItem value="768x1024">768x1024 (Portrait)</SelectItem>
                      <SelectItem value="1920x1080">1920x1080 (HD)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label htmlFor="num_images">Number of Images (1-4)</Label>
                <Input
                  id="num_images"
                  type="number"
                  min={1}
                  max={4}
                  value={numImages}
                  onChange={(e) => setNumImages(parseInt(e.target.value) || 1)}
                />
              </div>
            </CardContent>
          </Card>

          <Button
            onClick={handleGenerate}
            disabled={loading || loadingOptions}
            className="w-full"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Generating Images...
              </>
            ) : (
              <>
                <ImageIcon className="mr-2 h-4 w-4" />
                Generate Images
              </>
            )}
          </Button>
        </div>

        {/* Right Column - Results */}
        <div className="space-y-6">
          {/* Job Status */}
          {jobId && (
            <Card>
              <CardHeader>
                <CardTitle>Generation Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center space-x-2">
                  {jobStatus === "completed" && <CheckCircle2 className="h-5 w-5 text-green-500" />}
                  {jobStatus === "failed" && <XCircle className="h-5 w-5 text-red-500" />}
                  {jobStatus === "processing" && <Loader2 className="h-5 w-5 animate-spin" />}
                  <Badge variant={jobStatus === "completed" ? "default" : jobStatus === "failed" ? "destructive" : "secondary"}>
                    {jobStatus}
                  </Badge>
                </div>
                
                {jobId && (
                  <p className="text-sm text-muted-foreground">Job ID: {jobId}</p>
                )}

                {result?.processing_time && (
                  <p className="text-sm text-muted-foreground">
                    Processing Time: {result.processing_time.toFixed(2)}s
                  </p>
                )}
              </CardContent>
            </Card>
          )}

          {/* Generated Images */}
          {result?.images && result.images.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Generated Images ({result.images.length})</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {result.images.map((img, index) => (
                  <div key={img.image_id} className="space-y-2">
                    <div className="relative aspect-square w-full bg-muted rounded-lg overflow-hidden">
                      <img
                        src={img.url}
                        alt={`Generated image ${index + 1}`}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Crect fill='%23ddd' width='400' height='400'/%3E%3Ctext fill='%23999' font-family='sans-serif' font-size='20' dy='10.5' font-weight='bold' x='50%25' y='50%25' text-anchor='middle'%3EImage Loading...%3C/text%3E%3C/svg%3E";
                        }}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-mono text-muted-foreground truncate">
                        {img.image_id.substring(0, 8)}...
                      </p>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => window.open(img.url, '_blank')}
                      >
                        <Download className="h-4 w-4 mr-1" />
                        Download
                      </Button>
                    </div>
                    {img.metadata && (
                      <div className="text-xs text-muted-foreground">
                        {Object.entries(img.metadata)
                          .filter(([_, v]) => v)
                          .map(([k, v]) => (
                            <Badge key={k} variant="secondary" className="mr-1 mb-1">
                              {k}: {String(v)}
                            </Badge>
                          ))}
                      </div>
                    )}
                  </div>
                ))}
              </CardContent>
            </Card>
          )}

          {/* Enhanced Prompt Preview */}
          {result?.prompt && (
            <Card>
              <CardHeader>
                <CardTitle>Enhanced Prompt</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground">{result.prompt}</p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
