"""
Example: Basic Film Production Pipeline

This example demonstrates how to use the AI Film Studio
to produce a film from a script.
"""

from ai_film_studio import FilmPipeline
from ai_film_studio.utils import Config


def main() -> None:
    """Run a basic film production example."""
    # Create a simple script
    script = """
    FADE IN:

    INT. LIVING ROOM - DAY

    A cozy living room with sunlight streaming through the windows.

    ALICE sits on the couch, reading a book.

    ALICE
    This is going to be a great day.

    BOB enters through the front door.

    BOB
    Hey Alice! Ready for our adventure?

    FADE OUT.
    """

    # Initialize the pipeline
    pipeline = FilmPipeline()

    # Run the pipeline
    output = pipeline.run(script, output_name="my_film")

    print(f"Film produced: {output}")


if __name__ == "__main__":
    main()
