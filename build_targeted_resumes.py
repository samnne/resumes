"""Build role-targeted daughter resumes from the existing master (never modifies it)."""
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

SOURCE = Path('Samuel_Echefu_Software_Resume.tex')
OUT = Path('targeted_resumes')
OUT.mkdir(exist_ok=True)
source = SOURCE.read_text()
prefix = source.split('%-----------EDUCATION-----------')[0]
prefix = prefix.replace(r'\fancyfoot{}', r'\fancyfoot{}' + '\n' + r'\setlength{\footskip}{4pt}')

# Keep source project headings, including every supplied repository link.
project_blocks = source.split(r'\section{Projects}')[1].split('%-----------SKILLS-----------')[0]
headings = {}
for line in project_blocks.splitlines():
    if line.startswith(r'\resumeProjectHeading'):
        name = re.search(r'\\textbf\{([^}]+)\}', line).group(1)
        headings[name] = line

def tex(text):
    return (text.replace('&', r'\&').replace('%', r'\%')
            .replace('_', r'\_').replace('<', r'$<$'))

def bullets(items):
    return '\\resumeItemListStart\n' + ''.join(
        '  \\resumeItem{' + tex(item) + '}\n' for item in items
    ) + '\\resumeItemListEnd\n'

jobs = {
    'satellite': ('Software Engineer', 'Sep 2026 -- Present', 'UVic Satellite Design', 'Victoria, BC'),
    'aeternum': ('Software Developer', 'May 2026 -- Jul 2026', 'Aeternum Corp', 'Edmonton, AB'),
    'properseer': ('Frontend Developer', 'May 2025 -- Sep 2025', 'ProperSeer', 'Calgary, AB'),
}
work = {
    'satellite': [
        'Built an \\textbf{SPI} video pipeline across an \\textbf{nRF5340}, \\textbf{Raspberry Pi}, and host laptop using \\textbf{FreeRTOS}, C, and \\textbf{Python} to chunk frames and stream in real time.',
    ],
    'aeternum': [
        'Shipped a permission-first RAG prototype with \\textbf{FastAPI} and \\textbf{TypeScript} ahead of deadline, applying a 90% confidence threshold to response generation.',
        'Created a dashboard \\textbf{API} that batched metric requests, reduced network overhead, and cut latency by 70%.',
    ],
    'properseer': [
        'Built responsive property-management dashboards with \\textbf{React}, \\textbf{Redux}, and \\textbf{Bootstrap}; used memoization and prefetching to improve page load time by 20%.',
    ],
}
projects = {
    'MarketQuad': [
        'Launched a \\textbf{Next.js} marketplace serving 20+ UVic students; implemented \\textbf{Supabase} authentication and \\textbf{PostgreSQL} row-level security with @uvic.ca email restrictions.',
        'Load-tested the \\textbf{Next.js} \\textbf{API} with \\textbf{Locust}, sustaining \textbf{p95} $<$ \textbf{500 ms} at 1500+ requests/second.',
        'Added \\textbf{Socket.io} messaging and \\textbf{Cloudinary} CDN delivery; image prefetching reduced listing load times by 10%.',
    ],
    'Morph': [
        'Built a \\textbf{Python} AI agent harness with a \\textbf{Textual} conversation UI, \\textbf{asyncio}, and an agentic tool-calling loop over the \\textbf{OpenAI Responses \\textbf{API}}.',
        'Integrated \\textbf{MCP} servers over stdio, discovering external tools at startup and routing calls alongside 5 local tools (8 tools total).',
        'Added command allowlisting, path-traversal rejection, 30-second timeouts, and output truncation, plus persistent user memory and runtime workspace switching.',
    ],
    'uTransit': [
        "Built a Go service to decode BC Transit's GTFS Realtime Protobuf feed into live vehicle positions and trip updates for a React Native app.",
        'Reduced API latency from \\textbf{650 ms} to \\textbf{45 ms} with in-memory caching and indexed lookups; recorded \\textbf{p99} $<$ \\textbf{320 ms} with 1000 simulated users over 5 minutes in Locust.',
        'Batched and memoized mobile network calls to improve round-trip response time by 25%.',
    ],
    'Benny': [
        'Built a Spring Boot receipt-parsing backend that uses the Gemini API to extract line items and classify expenses and spending trends into Firestore.',
        'Developed a React Native app and TypeScript data pipeline to visualize expense metrics with Tailwind and estimate grocery totals using weighted averages.',
    ],
    'Multi-Threaded Job Scheduler': [
        'Built a C scheduler with pthreads to simulate up to 256 concurrent threads using priority scheduling and mutual exclusion.',
        'Implemented four FIFO queues with directional and priority tie-breaking rules and starvation prevention; checked scheduling output against expectations using Python.',
    ],
    'uEyes': [
        "Built a Gemini-powered computer vision app for Google AI Studio's hackathon, describing a user's environment with audio in \\textbf{500 ms} using short context windows.",
        'Used WebSockets, FastAPI, Firebase, React, and Tailwind for real-time interaction; containerized the backend with Docker and deployed it to Google Cloud Platform.',
    ],
    'Simple Shell Interpreter - Operating Systems Course': [
        'Built a C shell that executes built-in commands and programs on PATH, using process-creation system calls and supporting background tasks.',
        'Implemented persistent command history, Git support, and custom data structures to track background processes and user commands.',
    ],
    'VST Fingers': [
        'Built a computer vision VST controller with Python, OpenCV, MediaPipe, and OSC messaging, mapping finger detection to controls inside Max9 in \\textbf{50 ms}.',
        'Co-authored a research paper on a computer vision music system that maps real-time finger detection to VSTs.',
    ],
    'Alert Me': [
        'Built an ESP32 smart camera with C++, Python, and OpenCV to capture live video for object detection.',
        'Integrated YOLO to detect people entering the camera view and trigger alerts.',
    ],
    'Hash Table Experimental Analysis': [
        'Implemented hash tables in C, Java, and Python to compare chaining and linear probing across large table sizes.',
        'Standardized comparisons with a Jenkins Hash implementation and analyzed the effects of language architecture and collision strategy on performance.',
    ],
    'OceanBloom': [
        "Explored Ocean Networks Canada's API through a structured learning plan in Google Colab; used Python, Pandas, Matplotlib, and Jupyter Notebook for data visualization.",
    ],
}

roles = [
    {
        'slug': 'Software_Engineer_Full_Stack',
        'title': 'Software Engineer | Full-Stack Developer',
        'targets': 'Software Engineer, Software Developer, Full-Stack Developer',
        'focus': 'End-to-end delivery, API performance, authentication, and user-facing applications.',
        'courses': 'Data Structures and Algorithms, Operating Systems, Software Systems Development, Software Development Methods',
        'skills': [
            ('Languages', 'TypeScript, JavaScript, Python, Go, Java, SQL, C/C++'),
            ('Frameworks', 'React, Next.js, React Native, FastAPI, Spring Boot, Node.js, Tailwind'),
            ('Data & Tools', 'PostgreSQL, Supabase, Firebase, Git/GitHub, Docker, Linux, Locust, Jest'),
        ],
        'projects': ['MarketQuad', 'uTransit', 'Morph'],
    },
    {
        'slug': 'AI_Product_Engineer',
        'title': 'AI Product Engineer | Applied AI Developer',
        'targets': 'AI Product Engineer, Applied AI Developer, AI Application Developer',
        'focus': 'LLM applications, RAG delivery, tool orchestration, and useful AI interfaces rather than model-training claims.',
        'courses': 'Intro to Artificial Intelligence, Probability and Statistics, Data Structures and Algorithms, Software Systems Development',
        'skills': [
            ('Languages', 'Python, TypeScript, JavaScript, Java, SQL'),
            ('AI & Applications', 'OpenAI API, Gemini API, MCP, RAG, FastAPI, Textual, asyncio, React Native, Spring Boot'),
            ('Data & Tools', 'Firebase, Firestore, PostgreSQL, Docker, Google Cloud Platform, Git/GitHub'),
        ],
        'work': {
            'aeternum': [
                'Shipped a permission-first RAG prototype using \\textbf{FastAPI} and \\textbf{TypeScript} ahead of deadline, applying a 90% confidence threshold to response generation.',
                'Translated a \\textbf{Figma} prototype into a \\textbf{React Native} client to display data and responses; built a batched dashboard \\textbf{API} that cut latency by 70%.',
            ],
        },
        'projects': ['Morph', 'Benny', 'uEyes'],
    },
    {
        'slug': 'Embedded_Firmware_Engineer',
        'title': 'Embedded Software Engineer | Firmware Developer',
        'targets': 'Embedded Software Engineer, Firmware Developer, Embedded Systems Intern',
        'focus': 'Microcontrollers, SPI telemetry, FreeRTOS, C/C++, concurrency, and hardware-connected vision.',
        'courses': 'Operating Systems, Data Structures and Algorithms, Software Systems Development, Calculus I-IV',
        'skills': [
            ('Languages', 'C/C++, Python, Bash, Java'),
            ('Embedded & Systems', 'FreeRTOS, SPI, nRF5340, Raspberry Pi, ESP32, pthreads, Linux, Make'),
            ('Vision & Tools', 'OpenCV, YOLO, MediaPipe, Git/GitHub'),
        ],
        'work': {
            'satellite': [
                'Built a high-speed \\textbf{SPI} video pipeline between an \\textbf{nRF5340}, \\textbf{Raspberry Pi}, and host laptop using \\textbf{FreeRTOS}, C, and \\textbf{Python} to chunk and stream frames in real time.',
                'Soldered hardware components for \\textbf{Raspberry Pi}-based relaying of \\textbf{SPI} telemetry and video packets to a host PC.',
            ],
            'aeternum': [
                'Built a \\textbf{FastAPI} dashboard \\textbf{API} that batched metric requests, reduced network overhead, and cut latency by 70%.',
            ],
        },
        'projects': ['Multi-Threaded Job Scheduler', 'Alert Me', 'VST Fingers'],
    },
    {
        'slug': 'Research_Software_Developer',
        'title': 'Research Software Developer | Computer Vision',
        'targets': 'Research Software Developer, Undergraduate Research Assistant, Computer Vision Research Intern',
        'focus': 'Research co-authorship, experimental comparisons, scientific data exploration, and real-time vision.',
        'courses': 'Intro to Artificial Intelligence, Probability and Statistics, Calculus I-IV, Data Structures and Algorithms',
        'skills': [
            ('Languages', 'Python, C/C++, Java, SQL'),
            ('Research & Data', 'Pandas, Matplotlib, Jupyter Notebook, Google Colab, OpenCV, MediaPipe'),
            ('Systems & Tools', 'Linux, pthreads, Git/GitHub, Locust, Google Cloud Platform'),
        ],
        'projects': ['VST Fingers', 'Hash Table Experimental Analysis', 'OceanBloom'],
    },
    {
        'slug': 'Systems_Software_Engineer',
        'title': 'Systems Software Engineer | Developer Tools',
        'targets': 'Systems Software Engineer, Systems Developer, Developer Tools Engineer',
        'focus': 'Concurrency, process management, OS concepts, command execution boundaries, and hardware data movement.',
        'courses': 'Operating Systems, Data Structures and Algorithms, Software Systems Development, Software Development Methods',
        'skills': [
            ('Languages', 'C/C++, Python, Go, Bash, Java'),
            ('Systems', 'Linux, pthreads, FreeRTOS, SPI, asyncio, MCP, Make'),
            ('Tools & Testing', 'Git/GitHub, Docker, Locust, JUnit, Jest'),
        ],
        'projects': ['Multi-Threaded Job Scheduler', 'Simple Shell Interpreter - Operating Systems Course', 'Morph'],
    },
    {
        'slug': 'Frontend_Mobile_Developer',
        'title': 'Frontend Developer | React Native Developer',
        'targets': 'Frontend Developer, React Developer, React Native Developer, Mobile Developer',
        'focus': 'React interfaces, mobile delivery, state management, image delivery, and client-side performance.',
        'courses': 'Software Systems Development, Software Development Methods, Data Structures and Algorithms',
        'skills': [
            ('Languages', 'TypeScript, JavaScript, Python, SQL'),
            ('Frontend & Mobile', 'React, React Native, Expo SDK, Next.js, Redux, Bootstrap, Tailwind, Socket.io'),
            ('Data & Tools', 'Supabase, Firebase, Cloudinary, Figma, Git/GitHub, Jest'),
        ],
        'work': {
            'aeternum': [
                'Designed and ported a \\textbf{Figma} prototype into a \\textbf{React Native} mobile client to display data and responses.',
                'Built a dashboard \\textbf{API} that batched metric requests and reduced latency by 70%; delivered a \\textbf{FastAPI} and \\textbf{TypeScript} RAG prototype ahead of deadline.',
            ],
            'properseer': [
                'Created responsive interfaces with \\textbf{React}, \\textbf{Redux}, and \\textbf{Bootstrap}, improving page load time by 20% through memoization and prefetching.',
                'Developed property-management dashboard views with \\textbf{React} and \\textbf{Redux} to streamline user workflows across device sizes.',
            ],
        },
        'project_bullets': {
            'MarketQuad': [
                'Launched a \\textbf{Next.js} marketplace serving 20+ UVic students, with \\textbf{Supabase} authentication restricted to @uvic.ca email addresses.',
                'Added real-time \\textbf{Socket.io} messaging and optimized \\textbf{Cloudinary} image delivery with CDN use and prefetching, reducing listing load times by 10%.',
            ],
            'uTransit': [
                'Built a mobile-first \\textbf{React Native} interface for live transit positions and trip updates backed by a \\textbf{Go} GTFS Realtime parser.',
                'Batched and memoized network calls to improve round-trip response time by 25%.',
            ],
        },
        'projects': ['MarketQuad', 'uTransit', 'Benny'],
    },
    {
        'slug': 'Backend_Software_Engineer',
        'title': 'Backend Software Engineer | API Developer',
        'targets': 'Backend Software Engineer, Backend Developer, API Developer',
        'focus': 'Go and Python services, caching, load testing, database authorization, and data ingestion.',
        'courses': 'Data Structures and Algorithms, Operating Systems, Software Systems Development, Probability and Statistics',
        'skills': [
            ('Languages', 'Go, Python, Java, TypeScript, SQL, Bash'),
            ('Backend', 'FastAPI, Spring Boot, Next.js, Node.js, Express.js, REST APIs, Protobuf, Socket.io'),
            ('Data & Tools', 'PostgreSQL, Supabase, Firebase, Docker, Linux, Locust, Git/GitHub'),
        ],
        'projects': ['uTransit', 'MarketQuad', 'Benny'],
    },
    {
        'slug': 'DevOps_Platform_Engineer',
        'title': 'DevOps / Platform Engineering | Cloud Applications',
        'targets': 'DevOps Intern, Junior Platform Engineer, Cloud Application Developer',
        'focus': 'Docker/GCP deployment, Linux, load testing, runtime controls, and service performance; no unsupported CI/CD or infrastructure-as-code claims.',
        'courses': 'Operating Systems, Software Systems Development, Data Structures and Algorithms, Software Development Methods',
        'skills': [
            ('Languages', 'Python, Go, Bash, TypeScript, SQL'),
            ('Cloud & Runtime', 'Docker, Google Cloud Platform, Linux, Git/GitHub, asyncio, MCP'),
            ('Services & Testing', 'FastAPI, REST APIs, Protobuf, Locust, PostgreSQL, Firebase'),
        ],
        'project_bullets': {
            'uEyes': [
                'Containerized a \\textbf{FastAPI} backend with \\textbf{Docker} and deployed it to \\textbf{Google Cloud Platform} for a real-time computer vision application.',
                'Connected \\textbf{React} clients through \\textbf{WebSockets} and \\textbf{Firebase}; used the \\textbf{Gemini API} and short context windows to deliver environment descriptions with audio in \textbf{500 ms}.',
            ],
            'Morph': [
                'Integrated \\textbf{MCP} servers over stdio with startup tool discovery and routing alongside local filesystem and command tools (8 tools total).',
                'Applied executable allowlisting, path-traversal rejection, 30-second command timeouts, and output truncation; added runtime workspace switching.',
            ],
        },
        'projects': ['uEyes', 'uTransit', 'Morph'],
    },
]

# Preserve every work-experience item verbatim from the master in all variants.
experience_section = source.split(r'\section{Work Experience}')[1].split('%-----------PROJECTS-----------')[0]
experience_chunks = {}
for match in re.finditer(r'(\\resumeSubheading\{([^}]+)\}\{[^}]+\}\{([^}]+)\}\{[^}]+\}.*?\\resumeItemListEnd)', experience_section, re.S):
    company = match.group(3)
    key = {'UVic Satellite Design': 'satellite', 'Aeternum Corp': 'aeternum', 'ProperSeer': 'properseer'}[company]
    experience_chunks[key] = match.group(1) + '\n'
assert set(experience_chunks) == set(jobs), 'Could not read all master work entries'

compiler = shutil.which('pdflatex')
results = []
for role in roles:
    title = role['title'].replace('|', r'$|$')
    start = prefix.replace(
        r'\textbf{\Huge \scshape Samuel Echefu} \\ \vspace{5pt}',
        r'\textbf{\Huge \scshape Samuel Echefu} \\ \vspace{3pt}' + '\n    ' +
        r'\small ' + title + r' \\ \vspace{3pt}'
    )
    chunks = [start, '\\section{Education}\n\\resumeSubHeadingListStart\n',
              r'\resumeSubheading{University of Victoria (UVIC)}{Sep 2024 -- Apr 2028}{Bachelor of Science in Computer Science (3rd year)}{}' + '\n',
              bullets(['Relevant Coursework: ' + role['courses']]),
              '\\resumeSubHeadingListEnd\n\n\\section{Technical Skills}\n',
              ' \\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n']
    skill_lines = []
    for label, value in role['skills']:
        skill_lines.append('     \\textbf{' + tex(label) + '}{: ' + tex(value) + '}')
    chunks.append(' \\\\ \\vspace{0pt}\n'.join(skill_lines))
    chunks.append('\n    }}\n \\end{itemize}\n\n\\section{Work Experience}\n\\resumeSubHeadingListStart\n')
    for key in ['satellite', 'aeternum', 'properseer']:
        chunks.append(experience_chunks[key])
    chunks.append('\\resumeSubHeadingListEnd\n\n\\section{Selected Projects}\n\\resumeSubHeadingListStart\n')
    for name in role['projects']:
        chunks.append(headings[name] + '\n')
        chunks.append(bullets(role.get('project_bullets', {}).get(name, projects[name])))
    chunks.append('\\resumeSubHeadingListEnd\n\\end{document}\n')
    filename = 'Samuel_Echefu_' + role['slug']
    path = OUT / (filename + '.tex')
    path.write_text(''.join(chunks))
    result = {'name': filename, 'pages': None}
    if compiler:
        for _ in range(2):
            proc = subprocess.run([compiler, '-interaction=nonstopmode', '-halt-on-error', path.name], cwd=OUT, capture_output=True, text=True)
            if proc.returncode:
                print(proc.stdout[-5000:])
                raise RuntimeError('Compilation failed: ' + str(path))
        log = (OUT / (filename + '.log')).read_text()
        match = re.search(r'Output written on .*?\((\d+) page', log, re.S)
        result['pages'] = int(match.group(1)) if match else None
        result['overfull'] = 'Overfull' in log
    results.append(result)

# Fill available page space with real source details, never by dropping work items.
# Try complete project entries, then fuller source versions of selected projects.
source_projects = {}
for match in re.finditer(r'(\\resumeProjectHeading[^\n]+\n\\resumeItemListStart\n.*?\\resumeItemListEnd)', project_blocks, re.S):
    name = re.search(r'\\textbf\{([^}]+)\}', match.group(1)).group(1)
    source_projects[name] = match.group(1)
assert len(source_projects) == 12
extra_projects = {
    'Software_Engineer_Full_Stack': ['Benny', 'uEyes'],
    'AI_Product_Engineer': ['VST Fingers', 'MarketQuad'],
    'Embedded_Firmware_Engineer': ['Simple Shell Interpreter - Operating Systems Course', 'Hash Table Experimental Analysis'],
    'Research_Software_Developer': ['uEyes', 'Multi-Threaded Job Scheduler'],
    'Systems_Software_Engineer': ['Hash Table Experimental Analysis', 'uTransit'],
    'Frontend_Mobile_Developer': ['uEyes', 'Morph'],
    'Backend_Software_Engineer': ['Morph', 'uEyes'],
    'DevOps_Platform_Engineer': ['Simple Shell Interpreter - Operating Systems Course', 'MarketQuad'],
}

def inspect_pdf(path):
    doc = ET.fromstring(subprocess.check_output(['pdftotext', '-bbox', str(path), '-'], text=True))
    pages = [e for e in doc.iter() if e.tag.endswith('page')]
    words = [e for e in doc.iter() if e.tag.endswith('word')]
    return len(pages), max(float(w.attrib['yMax']) for w in words)

def compile_draft(path, content):
    path.write_text(content)
    proc = subprocess.run([compiler, '-interaction=nonstopmode', '-halt-on-error', path.name], cwd=OUT, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stdout[-4000:])
    return inspect_pdf(path.with_suffix('.pdf'))

if compiler and shutil.which('pdftotext'):
    for role, result in zip(roles, results):
        path = OUT / (result['name'] + '.tex')
        content = path.read_text()
        pages, bottom = inspect_pdf(path.with_suffix('.pdf'))
        selected = list(role['projects'])
        # Add another complete project when there is room, even if less central to the role.
        for name in extra_projects[role['slug']]:
            ending = '\\resumeSubHeadingListEnd\n\\end{document}'
            candidate = content.replace(ending, source_projects[name] + '\n' + ending)
            trial_pages, trial_bottom = compile_draft(path, candidate)
            if trial_pages == 1 and trial_bottom <= 742:
                content, bottom = candidate, trial_bottom
                selected.append(name)
        # Restore fuller original bullet lists wherever the remaining space permits.
        for name in selected:
            pattern = r'\\resumeProjectHeading[^\n]+\n\\resumeItemListStart\n.*?\\resumeItemListEnd'
            def fuller(match):
                found = re.search(r'\\textbf\{([^}]+)\}', match.group(0)).group(1)
                return source_projects[name] if found == name else match.group(0)
            candidate = re.sub(pattern, fuller, content, flags=re.S)
            if candidate == content:
                continue
            trial_pages, trial_bottom = compile_draft(path, candidate)
            if trial_pages == 1 and bottom <= trial_bottom <= 742:
                content, bottom = candidate, trial_bottom
        # Modest bullet spacing uses the last small gap without shrinking fonts.
        base_content = content
        for step in range(-8, 13):
            itemsep = step * 0.15
            candidate = base_content.replace('itemsep=0pt', f'itemsep={itemsep:.2f}pt')
            trial_pages, trial_bottom = compile_draft(path, candidate)
            if trial_pages != 1 or trial_bottom > 742:
                continue
            if trial_bottom >= bottom or step == 0:
                content, bottom = candidate, trial_bottom
        # Back off extra projects if still overflowing the text area.
        while bottom > 742 and len(selected) > len(role['projects']):
            drop = selected.pop()
            pattern = r'\\resumeProjectHeading[^\n]+\n\\resumeItemListStart\n.*?\\resumeItemListEnd\n?'
            blocks = list(re.finditer(pattern, content, re.S))
            for m in reversed(blocks):
                found = re.search(r'\\textbf\{([^}]+)\}', m.group(0))
                if found and found.group(1) == drop:
                    content = content[:m.start()] + content[m.end():]
                    break
            pages, bottom = compile_draft(path, content)
        compile_draft(path, content)
        compile_draft(path, content)  # Resolve hyperlink outlines after final pagination.
        log = path.with_suffix('.log').read_text()
        assert 'Overfull' not in log, path
        for key, chunk in experience_chunks.items():
            assert chunk.strip() in content, (path, key)
        result.update(pages=1, bottom=round(bottom, 1), projects=selected, work_items=8, overfull=False)

readme = ['# Targeted resumes\n',
          'Source: `../Samuel_Echefu_Software_Resume.tex` (left unchanged).\n',
          'Eight tailored daughter resumes with selected projects, reordered skills, and the supplied GitHub links. All eight original work-experience bullets are preserved verbatim in every version; fuller project details and additional complete projects use the available page space, even where less central to the target role. Original employers, job titles, dates, and reported metrics are preserved; no retail or soft-skills sections are included.\n',
          '| File (`.tex` / `.pdf`) | Target roles | Emphasis |\n| --- | --- | --- |']
for role, result in zip(roles, results):
    readme.append('| `'+result['name']+'` | '+role['targets']+' | '+role['focus']+' |')
readme += ['\n## Notes\n',
           '- All work-experience list items are retained. Pages are filled with additional source project material, then modest bullet spacing; no text is clipped and fonts are not reduced.',
           '- These are internship / early-career variants, not claims of seniority in each discipline.',
           '- The AI version targets application/product engineering, not unsubstantiated ML model-training experience.',
           '- The DevOps/platform version emphasizes demonstrated Docker/GCP deployment and Linux/service work. The source does not establish CI/CD pipelines, Kubernetes, Terraform, on-call operations, or production infrastructure ownership.',
           '- The research version preserves research co-authorship without implying publication, peer review, or a formal research appointment.',
           '- Alert Me and Multi-Threaded Job Scheduler remain unlinked because the source has no repository URLs for them.',
           '- Dates and third-year status are copied from the master. Confirm they match your application date before submitting.',
           '- Reported performance figures are retained from the master, not independently verified. Be prepared to explain test conditions.',
           '\n## Build\n',
           'From this directory, run `pdflatex -interaction=nonstopmode -halt-on-error <filename>.tex` twice. Alternatively, run `python build_targeted_resumes.py` from the workspace root to regenerate all variants from the curated definitions.']
(OUT / 'README.md').write_text('\n'.join(readme) + '\n')
for result in results:
    print(result)
