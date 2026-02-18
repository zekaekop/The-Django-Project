<h1>How to?</h1>

<ul>
    <b>
    <li><a href="#icons">Adding icons</a></li>
    </b>
</ul>

<h3 id="icons"> How to add icons to the project</h3>
<p>First add your icons into the static/img/ folder where they belong,
after this you shjould refrence and declare variables for them in the base files according on what part of the icon u want them to show in, or you could add them to all of the base files meaning it will show everywhere.</p>

```
--favorite-heart: url("{% static 'img/profile/favorite_heart.svg' %}");
```
<hr>

"--favorite-heart" variable
<br>
"img/profile/favorite_heart.svg" refrence

<hr>

<p>When refrencing in the base.html file you should declare it a variable for both light and dark mode (note this could be for multiple other themes possibly in the future).</p>

<p>After this you should go to static/css/icons, this is where you can add the refrenced icon to a class where you will be able to call the class on a image to use it according to what base file its located in.</p>