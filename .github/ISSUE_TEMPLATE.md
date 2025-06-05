---
name: Feature request or issue
description: Suggest a change to the taxonomy, tooling, or documentation
title: "[Suggestion] <Your summary here>"
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this issue!
  - type: textarea
    id: description
    attributes:
      label: Description
      description: Please describe what you'd like to see improved or changed.
      placeholder: Tell us what you'd like to see improved...
    validations:
      required: true
  - type: textarea
    id: proposed-change
    attributes:
      label: Proposed Change
      description: How would you improve the taxonomy or tooling?
      placeholder: Describe your proposed changes...
    validations:
      required: true
  - type: textarea
    id: additional-context
    attributes:
      label: Additional Context
      description: Optional screenshots, examples, or references
      placeholder: Add any other context about the suggestion here...
    validations:
      required: false
---

## Description

Please describe what you'd like to see improved or changed.

## Proposed Change

How would you improve the taxonomy or tooling?

## Additional Context

(Optional screenshots, examples, or references)
