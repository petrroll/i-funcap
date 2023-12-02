## What is it?

WIP of unofficial interactive version of [FUNCAP pre-print](https://www.preprints.org/manuscript/202309.2091/v1) [questionnaire](https://www.preprints.org/manuscript/202309.2091/v1/download/supplementary) for assessing ME/CFS.

## How does it work?

`generate.py` generates individual variants (`./output/funcap.<lang>.<variant>.html`) based on `./templates/*.template.html` files and language and variant specific questions in `/langs`. Currently very WIP, i.e. most questions are missing, there's no comparison with published cohorts, etc.

Despite being WIP, any PRs welcome!

## Plan (feel free to contribute before I add it)
- add general description, add explanation of values (WIP)
- rework UI/UX (I'm really not good at that, so please help) of the form itself
- show where you fall in comparison with other people based on the data reported in the paper 
- ask authors if its ok?
- storing intermediate results in local storage so that one can fill in not in one go
- add proper header with language and type selection instead of the awful approach with index.html
- ~rip all questions for english~ (thanks!), and some other language variant
- ~make it available on githubio domain or maybe under petrroll.cz somewhere?~ -> http://petrroll.cz/i-funcap/ for now
- ~add support for generating 55 and 27 questions versions~ -> should be improved

## Current stack

Pure HTML and vanilla js stitched together via python script that "templates". Want to keep it serverless to host on GitHub pages or so. If we decide to store results somewhere let's go API route and eg azure function or smth. The idea was to keep it as simple as possible hence no JS framework, no serverside, nothing.

But as said, happy to be convinced that something shinnier would be better.

