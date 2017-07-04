# BabyBrowser
Browser Project

Forked from [LB's BabyBrowser](https://github.com/lauryndbrown/BabyBrowser). Due to issues with the git commit history I had to detach my fork.


Note on rebuilding the bookmarks pickle:

```
f = [MenuWebPage('https://raw.githubusercontent.com/lauryndbrown/BabyBrowser/master/baby_browser/Examples/paragraphs.html', 'Paragraphs Example'),
     MenuWebPage('https://raw.githubusercontent.com/lauryndbrown/BabyBrowser/master/baby_browser/Examples/headers2.html', 'Header Example'),
     MenuWebPage('https://raw.githubusercontent.com/lauryndbrown/BabyBrowser/master/baby_browser/Examples/image.html', 'Image Example'),
     MenuWebPage('https://raw.githubusercontent.com/lauryndbrown/BabyBrowser/master/baby_browser/Examples/paragraphs_with_style.html', 'Head Styles Example'),
     MenuWebPage('https://raw.githubusercontent.com/lauryndbrown/BabyBrowser/master/baby_browser/Examples/hr.html', 'HR Example'),
     MenuWebPage('https://raw.githubusercontent.com/lauryndbrown/BabyBrowser/master/baby_browser/Examples/spaces_in_p.html', 'Spaces Example')]
pickle.dump(f, bookmarks_file, protocol=pickle.HIGHEST_PROTOCOL)
```

License:

LB has not listed a anything on the main repo, so I am unable to correctly license my code for now.
