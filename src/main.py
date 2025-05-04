"""
Main entry point for the AI Blog Writer application.
"""

import logging
from pathlib import Path
import sys
from typing import Optional

import click

from src.pipeline.pipeline_runner import PipelineRunner
from src.utils.logger import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def validate_input_file(ctx, param, value):
    """Validate that the input file exists."""
    if value:
        if not Path(value).exists():
            raise click.BadParameter(f"Input file {value} does not exist")
    return value

@click.command()
@click.option(
    "--input-file",
    type=click.Path(exists=True),
    help="Path to input JSON file containing blog specifications",
    callback=validate_input_file,
)
@click.option(
    "--output-file",
    type=click.Path(),
    help="Path to output JSON file for generated content",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug mode",
)
def main(input_file: Optional[str], output_file: Optional[str], debug: bool):
    """
    Run the AI Blog Writer pipeline.
    
    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file
        debug: Enable debug mode
    """
    try:
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")

        # Initialize pipeline runner
        pipeline_runner = PipelineRunner()
        
        # Run pipeline
        if input_file:
            result = pipeline_runner.run_from_file(input_file)
            if output_file:
                with open(output_file, "w") as f:
                    f.write(result.json())
                logger.info(f"Output written to {output_file}")
            else:
                print(result.json())
        else:
            click.echo("No input file provided. Use --help for usage.")

    except Exception as e:
        logger.error(f"Error running pipeline: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
