# Project Workflow

This file isn't a part of the project, the best way to describe it is it's just some sort of diary

so my workflow throughout engineering was by pasting a random file I pick out of the ./engineering/data/ directory into
regex101.com, and start finding out how can I extract the feature I'm currently working on. then I execute that regex on
all of the files in python, and print the filename, and the feature I'm looking onto

```python
for file in filenames:
	filecontent = read(file)
	search = re.findall(r"the regex", filecontent)
	print(file, "iusearch" if len(search) == 0 else search)
```

Here gnu/linux comes to the play, I print a string that I'm sure it would never exist in the whole project (e.g. iusearch)
and then I do `python main.py | grep iusearch`, then I get the filenames that missed that value, which was nice and
helped boost my productivity a lot.

Another example:

```python
for file in filenames:
	filecontent = read(file)
	search = re.findall(r"(part|full)-time", filecontent)
	print(file, search)
```

Here to get the count of the part time jobs I just did: `python main.py | grep "part-time" | wc -l`, and to get the full
time it was just replacing a word, no need to program a counter in python or a list with filenames being appended to. it
felt like a superpower I had in my hands!

Other commands I enjoyed using:
`ls -1 ./data/ | grep -l`

`python main.py | less`

`cat file.txt | wl-copy` (as I use wayland)

`python main.py | wc -l`
