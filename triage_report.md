# Systems Debug Report: PERC Connectivity Violations

## 1. Overall System Health
**Status: CRITICAL**
The system is experiencing a high volume of PERC (Programmable Electrical Rule Check) failures, with a total of **1,517 recorded errors**. The failures are concentrated in the `TOP MACRO` cell, specifically involving net violations. The presence of `GATE DIRECT FLOAT` and `PATH RES 02` suggests significant electrical connectivity or design rule integrity issues. 

## 2. Root Cause Analysis
Based on the provided documentation and failure patterns, the root cause is attributed to:

*   **Electrical Connectivity Violations:** Specific nets are failing Programmable Electrical Rule Checks (PERC). The errors identify specific failure points at coordinate locations `(<ID>.<ID> <ID>.<ID>)`.
*   **Expansion/Tracing Logic Failures:** The manual context (Lines 167–184) focuses on the syntax for expanding sets of cells and wires (`%x`, `%ci`, `%co`). The violations likely occur when the connectivity traversal—limited by inclusion (`+`) or exclusion (`-`) rules or object limits (`<num2>`)—detects illegal states like floating gates or path resistance issues.
*   **Limit Exhaustion:** Line 177 indicates a limit (`<num2>`) on selected objects during expansion. If this limit is reached, the analysis may be incomplete or trigger a warning, though the current evidence shows hard "FAIL" statuses.

## 3. Actionable Fix Steps
To resolve these violations, engineers must use the expansion syntax defined in the manual to trace the failing nets:

1.  **Trace Failing Nets (Connectivity Expansion):**
    Utilize the `%x` command to expand the net set from the reported coordinates.
    *   *Syntax:* `%x[*][.<num2>][:<rule>]`
    *   Use the `*` wildcard to repeat expansion until the full net path is identified to locate the source of the `GATE DIRECT FLOAT` or `PATH RES 02` error.

2.  **Define Inclusion/Exclusion Rules:**
    Refine the debugging expansion by applying rules to the cell ports (Lines 172-175).
    *   Use `+` followed by cell types and `[ports]` to include specific paths that should be tied to a driven signal.
    *   Use `-` to exclude paths that are known to be irrelevant to the current net failure.

3.  **Validate Input/Output Cones:**
    For `GATE DIRECT FLOAT` violations, use the `%ci` (input cone) expansion (Line 181) to verify if the gate has a valid input driver. For `PATH RES` violations, use `%co` (output cone) to trace the path to its destination.

4.  **Further Verification Required:**
    The provided documentation describes the *traversal syntax* but does not define the specific parameters for the rules `PATH RES 02` or `GATE DIRECT FLOAT`. Further documentation is required to understand the specific threshold for "PATH RES 02" (e.g., maximum resistance values) and the specific conditions that trigger "GATE DIRECT FLOAT" (e.g., tie-up/tie-down requirements).