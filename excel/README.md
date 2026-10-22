# Excel audit companion

Open `ThirstyAI_Audit.xlsx` in Excel or a compatible spreadsheet application. Calculator has a single editable input set (amber cells), formula-linked water/energy/carbon outputs and explicit missing-input handling. India contains the 36 government-reported rows, unchanged in meaning. Sources gives their evidence locators and URLs.

This workbook is an independent calculation view, not a Power BI file. Default inputs are illustrative. Consumption WUE and IT kWh denominator are fixed by the model definition; do not substitute a withdrawal factor. Changing IT workload from 1,000 to 2,000 MWh doubles the total from 2.2 to 4.4 million liters under the default factors. Blank required inputs show Invalid input. Core outputs were compared to the Python model and inspected for formula errors. Each sheet was rendered for visual QA. Native Excel Desktop was not available for a separate engine check.

The checked-in workbook is immediately usable. `scripts/build_workbook.mjs` records the authoring process and needs the authoring runtime's `@oai/artifact-tool`; it is not needed for normal project setup or offline reproduction of the core research pipeline. The public core has no such dependency. Do not run npm install expecting that authoring-only package to be installed by package.json.
