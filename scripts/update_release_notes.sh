#!/bin/bash
#
# Script to help with the SMQTK release process. Performs the following steps:
#   - Poetry version (major, minor, or patch)
#   - Rename release_notes/pending_release file to release_notes/version
#   - Add reference to new release notes file in release_notes.rst
#   - Add new release notes stub file
#
# Two git commits are created. One for the version bump and one for the new
# release notes stub file.
#
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${SCRIPT_DIR}/.."
DOCS_DIR="${PROJECT_DIR}/docs"
RELEASE_NOTES_DIR="${DOCS_DIR}/release_notes"

# Check args
if [ "$#" != 1 ]
then
  echo "Please enter valid version bump type. Options: major, minor, or patch"
  exit 1
fi

if [ "$1" != 'major' ] && [ "$1" != 'minor' ] && [ "$1" != 'patch' ]
then
  echo "Please enter valid version bump type. Options: major, minor, or patch"
  exit 1
fi

RELEASE_TYPE="$1"
echo "Release type: ${RELEASE_TYPE}"

# Update version
poetry version "${RELEASE_TYPE}"

# Get version
VERSION="$(poetry version -s)"
VERSION_STR="v${VERSION}"
VERSION_SEPERATOR=${VERSION_STR//?/=}

# Rename release notes to current version
git mv "${RELEASE_NOTES_DIR}"/pending_release.rst "${RELEASE_NOTES_DIR}"/"${VERSION_STR}".rst

# Replace pending release notes line
sed -i "s/Pending Release Notes/${VERSION_STR}/" "${RELEASE_NOTES_DIR}"/"${VERSION_STR}".rst
sed -i "s/=====================/${VERSION_SEPERATOR}/" "${RELEASE_NOTES_DIR}"/"${VERSION_STR}".rst

echo "Moved pending release notes to ${VERSION_STR}.rst"

# Add reference to new file in release_notes.rst
echo "   release_notes/${VERSION_STR}" >> "${DOCS_DIR}"/release_notes.rst
echo "Reference added to release_notes.rst"

# Make git commits
git add "${PROJECT_DIR}"/pyproject.toml
git add "${RELEASE_NOTES_DIR}"/v"${VERSION}".rst
git add "${DOCS_DIR}"/release_notes.rst
git commit -m "Update version number to ${VERSION}"

# Make new pending notes file
cp "${SCRIPT_DIR}"/.pending_notes_stub.rst "${RELEASE_NOTES_DIR}"/pending_release.rst

git add "${RELEASE_NOTES_DIR}"/pending_release.rst
git commit -m "Add pending release notes stub"
