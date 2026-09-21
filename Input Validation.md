# Input validation vulnerability

Input validation is a server-side security control. Browser checks can be bypassed by sending a request directly with Burp Suite, curl, or another client.

## Vulnerable behavior

The vulnerable function in `input_validation_lab.py` copies the submitted values without checking their type, length, format, or meaning:

```python
{
    "name": "<script>alert(1)</script>",
    "date_of_birth": "2026-02-31",
    "email": "not-an-email"
}
```

A real application might store these values, display them later, or pass them to another component. The input is not automatically safe just because it arrived in a form field. Depending on the surrounding application, this can lead to invalid records, stored script injection, log injection, downstream parser errors, or business-logic problems.

## Patch

The patched function validates the request on the server and returns field-level errors without echoing rejected values:

- Accept exactly `name`, `date_of_birth`, and `email`.
- Require text values and reject missing, null, empty, whitespace-only, and unexpected fields.
- Trim surrounding whitespace before validation.
- Allow names up to 100 characters, including Unicode letters, spaces, apostrophes, and hyphens. Reject markup-like characters, control characters, digits, and oversized names.
- Parse date of birth as an exact `YYYY-MM-DD` date. Reject impossible dates and dates after today. This example does not assume a minimum age.
- Limit email addresses to 254 characters, require one `@`, and validate a practical email format. Normalize the email to lowercase after validation.

The example uses a deliberately pragmatic email check. It is not a complete RFC 5322 implementation and does not prove that an address can receive mail.

## Run the demonstration

From this folder, run:

```text
python3 input_validation_lab.py
```

The output shows the same submitted data passing through both paths. The vulnerable path accepts malformed input; the patched path accepts only the valid record and reports generic validation errors for the invalid one.

## Testing lesson

Test server-side validation directly with missing fields, null values, wrong JSON types, extra fields, empty values, long values, invalid dates, future dates, malformed emails, and injection-shaped strings. A client-side form constraint is useful for user experience, but it is not an authorization or security boundary.
