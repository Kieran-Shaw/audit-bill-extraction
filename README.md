# audit-bill-extraction

A set of cloud functions to extract information from bills

## bill-metadata

This method extracts the metadata for the bill

- total_current_premium (the total premium on the bill w/out any retro charges applied)
- billing_start_date
- billing_end_Date

## gpt-extraction

This method uses GPT Assistants to extract the line items from the bill

# Commentary / Comments

- If GPT fails, should we build sensible extractions?

# To Do

1. Validations on the sensible extraction?
2. What happens when the sensible extraction fails / we don't get what we expected? How can we still return a response but have it be null / empty for those values?
