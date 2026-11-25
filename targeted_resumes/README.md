# Targeted resumes

Source: `../Samuel_Echefu_Software_Resume.tex` (left unchanged).

Eight tailored daughter resumes with selected projects, reordered skills, and the supplied GitHub links. All eight original work-experience bullets are preserved verbatim in every version; fuller project details and additional complete projects use the available page space, even where less central to the target role. Original employers, job titles, dates, and reported metrics are preserved; no retail or soft-skills sections are included.

| File (`.tex` / `.pdf`) | Target roles | Emphasis |
| --- | --- | --- |
| `Samuel_Echefu_Software_Engineer_Full_Stack` | Software Engineer, Software Developer, Full-Stack Developer | End-to-end delivery, API performance, authentication, and user-facing applications. |
| `Samuel_Echefu_AI_Product_Engineer` | AI Product Engineer, Applied AI Developer, AI Application Developer | LLM applications, RAG delivery, tool orchestration, and useful AI interfaces rather than model-training claims. |
| `Samuel_Echefu_Embedded_Firmware_Engineer` | Embedded Software Engineer, Firmware Developer, Embedded Systems Intern | Microcontrollers, SPI telemetry, FreeRTOS, C/C++, concurrency, and hardware-connected vision. |
| `Samuel_Echefu_Research_Software_Developer` | Research Software Developer, Undergraduate Research Assistant, Computer Vision Research Intern | Research co-authorship, experimental comparisons, scientific data exploration, and real-time vision. |
| `Samuel_Echefu_Systems_Software_Engineer` | Systems Software Engineer, Systems Developer, Developer Tools Engineer | Concurrency, process management, OS concepts, command execution boundaries, and hardware data movement. |
| `Samuel_Echefu_Frontend_Mobile_Developer` | Frontend Developer, React Developer, React Native Developer, Mobile Developer | React interfaces, mobile delivery, state management, image delivery, and client-side performance. |
| `Samuel_Echefu_Backend_Software_Engineer` | Backend Software Engineer, Backend Developer, API Developer | Go and Python services, caching, load testing, database authorization, and data ingestion. |
| `Samuel_Echefu_DevOps_Platform_Engineer` | DevOps Intern, Junior Platform Engineer, Cloud Application Developer | Docker/GCP deployment, Linux, load testing, runtime controls, and service performance; no unsupported CI/CD or infrastructure-as-code claims. |

## Notes

- All work-experience list items are retained. Pages are filled with additional source project material, then modest bullet spacing; no text is clipped and fonts are not reduced.
- These are internship / early-career variants, not claims of seniority in each discipline.
- The AI version targets application/product engineering, not unsubstantiated ML model-training experience.
- The DevOps/platform version emphasizes demonstrated Docker/GCP deployment and Linux/service work. The source does not establish CI/CD pipelines, Kubernetes, Terraform, on-call operations, or production infrastructure ownership.
- The research version preserves research co-authorship without implying publication, peer review, or a formal research appointment.
- Alert Me and Multi-Threaded Job Scheduler remain unlinked because the source has no repository URLs for them.
- Dates and third-year status are copied from the master. Confirm they match your application date before submitting.
- Reported performance figures are retained from the master, not independently verified. Be prepared to explain test conditions.

## Build

From this directory, run `pdflatex -interaction=nonstopmode -halt-on-error <filename>.tex` twice. Alternatively, run `python build_targeted_resumes.py` from the workspace root to regenerate all variants from the curated definitions.
