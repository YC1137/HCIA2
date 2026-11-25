
## Project Status

This Assignment 2 prototype turns an assignment brief into an ordered task plan. It shows a waiting message during generation and lets students open **View evidence** to compare each task with the original wording. The demonstrated workflow uses one brief at a time. The report examples cover plan generation and evidence inspection.

## Technology Stack

A single HTML page uses Vue 3 for interactivity. A local Python server numbers the brief's lines and sends them to the SiliconFlow Chat Completions API. The language model returns task titles and evidence line numbers. The server checks those numbers and retrieves the corresponding text from the brief. The live test used DeepSeek-V3.2.

## Run the Prototype

1. On Windows, install Python 3.9 or later with Tkinter. Download or clone this repository.
2. Double-click `Start-Assignment-Planner.pyw`. If prompted, enter your own SiliconFlow API key. The launcher opens the planner in your browser.
3. In the launcher, select **Change model** and enter `deepseek-ai/DeepSeek-V3.2`.
4. Use the example brief or paste your own. Select **Generate plan**, then open **View evidence** on a task.

Keep your API key and local configuration out of the repository. The brief is sent to SiliconFlow during generation.

## Development Record

- **Evidence.** The first version asked the model to reproduce quotations. Wording changes could cause tasks to be dropped. The revised version uses line numbers to retrieve exact excerpts. The main excerpts were checked against the Assignment 2 brief.
- **Task grouping.** An early test returned 12 tasks. A revised prompt grouped related requirements by deliverable. A later live test on the same brief returned five main tasks.

## AI Assistance

OpenAI Codex helped draft and revise the interface, API integration, and model prompt. Checks included running the planner with the Assignment 2 brief, comparing displayed evidence with the source, and reviewing the task list after the prompt change.
