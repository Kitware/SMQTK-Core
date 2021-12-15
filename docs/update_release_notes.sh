#!/bin/bash

# Check args
if [ $# != 1 ]
then
  echo "Please enter valid version bump type. Options: major, minor, or patch"
  exit 1
fi

if [ $1 != 'major' ] && [ $1 != 'minor' ] && [ $1 != 'patch' ]
then
  echo "Please enter valid version bump type. Options: major, minor, or patch"
  exit 1
fi

RELEASE_NOTES_PATH="release_notes"
RELEASE_TYPE=$1

# Update version
poetry version $1

# Get version
VERSION=$(poetry version -s)

echo "Current version: ${VERSION}"

# Rename release notes to current version
cp ${RELEASE_NOTES_PATH}/pending_release.rst ${RELEASE_NOTES_PATH}/v${VERSION}.rst

echo "Created v${VERSION}.rst"

# Add reference to new file in release_notes.rst
echo "   release_notes/v${VERSION}" >> release_notes.rst

echo "Reference added to release_notes.rst"

# Make new pending notes file
echo "Pending Release Notes" > ${RELEASE_NOTES_PATH}/pending_release.rst
echo "=====================\n" >> ${RELEASE_NOTES_PATH}/pending_release.rst
echo "Updates / New Features" >> ${RELEASE_NOTES_PATH}/pending_release.rst
echo "----------------------\n" >> ${RELEASE_NOTES_PATH}/pending_release.rst
echo "Fixes" >> ${RELEASE_NOTES_PATH}/pending_release.rst
echo "-----\n" >> ${RELEASE_NOTES_PATH}/pending_release.rst

# Make git commits
git add ../pyproject.toml
git add ${RELEASE_NOTES_PATH}/v${VERSION}.rst
git add release_notes.rst
git commit -m "Update version number to ${VERSION}"

git add ${RELEASE_NOTES_PATH}/pending_release.rst
git commit -m "Add pending release notes stub"
