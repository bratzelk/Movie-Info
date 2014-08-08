Contributing to Movie Info
=======================

 1. [Getting Involved](#getting-involved)
 2. [Reporting Bugs](#reporting-bugs)
 3. [Contributing Code](#contributing-code)
 4. [Improving Documentation](#improving-documentation)

## Getting Involved

I would love it if someone would like to contribute to this project!
You can help the project tremendously by discovering and [reporting bugs](#reporting-bugs),
[improving documentation](#improving-documentation), writing [GitHub issues](https://github.com/bratzelk/movie-info/issues),
or by adding your own features.

## Reporting Bugs

Before reporting a bug on the project's [issues page](https://github.com/bratzelk/movie-info/issues),
first make sure that your issue is caused by the application, not your application code
(e.g. passing incorrect arguments to methods, etc.).
Second, search the already reported issues for similar cases,
and if it's already reported, just add any additional details in the comments.

After you made sure that you have found a new bug,
here are some tips for creating a helpful report that will make fixing it much easier and quicker:

 * Write a **descriptive, specific title**. Bad: *Problem with polylines*. Good: *Doing X in IE9 causes Z*.
 * Include **browser, OS and Leaflet version** info in the description.
 * Create a **simple test case** that demonstrates the bug (e.g. using [JSFiddle](http://jsfiddle.net/)).
 * Check whether the bug can be reproduced in **other browsers**.
 * Check if the bug occurs in the stable version, master, or both.
 * *Bonus tip:* if the bug only appears in the master version but the stable version is fine,
   use `git bisect` to find the exact commit that introduced the bug.

## Contributing Code

### Considerations for Accepting Patches

I am happy to accept all patches! I'm commited to keeping the application relatively simple and lightweight, but feel free to go crazy.

Before sending a pull request with a new feature, first check if it's been discussed before already
(on [GitHub issues](https://github.com/bratzelk/movie-info/issues)).

If your feature or API improvement did get merged into master,
please consider submitting another pull request with the corresponding [documentation update](#improving-documentation).


### Making Changes to the Source

If you're not yet familiar with the way GitHub works (forking, pull requests, etc.),
be sure to check out the awesome [article about forking](https://help.github.com/articles/fork-a-repo)
on the GitHub Help website &mdash; it will get you started quickly.

You should always write each batch of changes (feature, bugfix, etc.) in **its own topic branch**.
Please do not commit to the `master` branch, or your unrelated changes will go into the same pull request.

You should also follow the code style and whitespace conventions of the original codebase (or write your own convention guide which we can all use).

Before commiting your changes, you should try to write tests where possible to ensure no bugs are committed.

Happy coding!

## Improving Documentation

The easiest way to make little improvements such as fixing typos without even leaving the browser
is by editing one of the files with the online GitHub editor:
browse the [gh-pages branch](https://github.com/bratzelk/movie-info/branches),
choose a certain file for editing (e.g. `README.md`),
click the Edit button, make changes and follow instructions from there.
Once it gets merged, the changes will immediately appear on the website.


## Thank You

I am really keen for others to contribute to this small project so don't be shy!
