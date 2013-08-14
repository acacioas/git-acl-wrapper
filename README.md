# git-acl-wrapper

git-http-backend ACL wrapper

## Why would I need this?

It's a simple way to do ACL over git repositories deployed under apache. If you've got a bunch of repositories and do not want do create hooks for *every* single git repository you have, using gitolite (or other authorization mechanisms), this may work for you :-)

### Usage example

Instead of setting the git's cgi script for git-http-backend, use this wrapper.

In your repository vhost, it will look like that:

```
SetEnv GIT_PROJECT_ROOT /git/repositories
SetEnv GIT_HTTP_EXPORT_ALL
ScriptAlias /git/ /usr/local/bin/git-acl-wrapper.cgi/
```

After that, you just have to create a **acl.conf** file for your repositories base, or repository. See:

```
$ ls /git/repositories/project1
acl.conf my_repos1.git my_repos2.git

$ ls /git/repositories/project1/my_repos1.git
acl.conf  branches  config  description  HEAD  hooks  info  objects  refs
```

The contents of acl.conf file must be a set of lines, each one of them containing a username, a comma, and a permission. 
See the example bellow:

```
$ cat acl.conf
user1, r
user2, rw

```

In this example:

user1 will have **only** read permisson. It'll be able to clone, pull, fetch, etc. But it won't be able to push anything 
user2 will have both read and write permission, so it'll be able to do anything.

**any** other user not listed in this file, won't have access for anything.

### Precedence of acl.conf

**An important tip is:**

If is there an **acl.conf** file inside the repository, it will be used, no matter what is defined on the project acl file.

### License

This wrapper is licensed under MIT License. So, feel free for used it,
with no restrictions (but I'm not responsible for it's usage in your code).

For more information, see the MIT-LICENSE.txt file

### Do you know (or want) to enhance this wrapper?

Please, feel free to fork it and push back to me your changes :-)
