# Twipeater


## Issue with Twint: "CRITICAL:twint.run:Twint:Feed:noDataExpecting"

This is a known issue with the Twin library. See [\[ERROR\] CRITICAL:twint.run:Twint:Feed:noDataExpecting ~ Inconsistent results [High Severity] #604 ](https://github.com/twintproject/twint/issues/604)

To solve this issue in the **dev environment** make sure to **not** install twint through the requirements files.
Instead run

`
pip install --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
`

To solve this issue on prod use the Dockerfile in this repo to install Twin
