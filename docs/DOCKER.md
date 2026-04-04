# Docker Support

This project includes Docker support for running CLI tools in a containerized environment.

## Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

### Using Docker Compose (Recommended)

#### Build and run the CLI tools container:

```bash
docker-compose up cli-tools
```

This will:
- Build the Docker image
- Start an interactive shell in the container
- Mount your local directory for file access

#### Run a specific CLI tool:

```bash
docker-compose run cli-tools python tools/clis/radiology_metrics.py --from 20240101 --to 20240107
```

#### Run tests in Docker:

```bash
docker-compose run test
```

### Using Docker directly

#### Build the image:

```bash
docker build -t clinical-skills-cli .
```

#### Run a CLI tool:

```bash
docker run -v $(pwd)/data:/data clinical-skills-cli python tools/clis/dicom_info.py /data/scan.dcm
```

#### Run an interactive shell:

```bash
docker run -it -v $(pwd):/app clinical-skills-cli /bin/bash
```

## Docker Compose Services

### cli-tools

Main service for running CLI tools interactively.

**Features:**
- Mounts local directory for file access
- Mounts data directory for DICOM files
- Runs as non-root user
- Interactive TTY support

### test

Service for running the test suite.

**Usage:**
```bash
docker-compose run test
```

## Volume Mounts

- `/app` - Application code (read-only from container)
- `/data` - Data directory for DICOM files

## Environment Variables

- `PYTHONPATH=/app` - Python module path
- `PYTHONUNBUFFERED=1` - Disable Python output buffering

## Examples

### Example 1: Analyze DICOM file

```bash
# Copy DICOM file to data directory
cp scan.dcm data/

# Run image QC analysis
docker-compose run cli-tools python tools/clis/image_qc.py data/scan.dcm
```

### Example 2: Generate radiology metrics

```bash
docker-compose run cli-tools python tools/clis/radiology_metrics.py --from 20240101 --to 20240107 --json
```

### Example 3: Search PubMed

```bash
docker-compose run cli-tools python tools/clis/pubmed_search.py "lung cancer" --max 10
```

## Development Workflow

### Rebuild after code changes:

```bash
docker-compose build --no-cache cli-tools
```

### View logs:

```bash
docker-compose logs cli-tools
```

### Stop all services:

```bash
docker-compose down
```

### Remove volumes:

```bash
docker-compose down -v
```

## Troubleshooting

### Permission denied errors

If you encounter permission issues with mounted volumes, ensure your user ID matches the container user (UID 1000). On Linux, you may need to adjust your user ID or use rootless Docker.

### Container won't start

Check if port conflicts exist or if the image build failed:
```bash
docker-compose logs cli-tools
docker ps -a
```

### Python module not found

Ensure the PYTHONPATH is set correctly and the code is mounted properly:
```bash
docker-compose run cli-tools python -c "import sys; print(sys.path)"
```

## Performance Considerations

- Docker adds overhead for I/O operations
- For processing large DICOM files, consider using bind mounts instead of volumes
- Use `--no-cache` flag when rebuilding after dependency changes

## Security Notes

- The container runs as a non-root user (appuser:1000)
- No secrets are baked into the image
- Use environment variables for sensitive configuration
- Regularly update base images for security patches
