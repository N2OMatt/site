#!/usr/bin/python
################################################################################
## File   : build.py                                                          ##
## Author : n2omatt - n2omatt@amazingcow.com                                  ##
## Date   : May 6, 2017                                                       ##
##                                                                            ##
## Description:                                                               ##
##   Call every underlying build script need to build the whole site.         ##
##   This way we have nice separation of the build scripts, since each of     ##
##   them only needs to know about the very part that they're building.       ##
##                                                                            ##
##   All build systems put the result on the _Output directory located on     ##
##   the same level from the build script. So what we need to do is:          ##
##      1 - Call the build script                                             ##
##      2 - Copy the _Output directory                                        ##
##      3 - Drink a cup of coffee :D                                          ##
################################################################################

################################################################################
## Imports                                                                    ##
################################################################################
import os;
import os.path;
import urllib;
import json;


################################################################################
## Helper Functions                                                           ##
################################################################################
def call_build_script(path):
    curr_path = os.getcwd();
    os.chdir(path);

    if(os.path.exists("build.py")):
        os.system("./build.py");
    elif(os.path.exists("build.sh")):
        os.system("./build.sh");

    os.chdir(curr_path);

def copy_build_script_output(path):
    os.system("mkdir -p ./_Output/{0}".format(path));
    os.system("cp -rf ./{0}/_Output/* ./_Output/{0}".format(path));


def read_file_text(filename):
    entry_file = open(filename);
    all_lines  = entry_file.readlines();

    entry_file.close();

    return "".join(all_lines);

def write_file_text(blog_entry_fullpath, text):
    outfile  = open(blog_entry_fullpath, "w");

    outfile.write(text);
    outfile.close();

def replace_index_template_contents(template, blog_entries, projects, certs):
    return template.replace(
        "__TEMPLATE_REPLACE_BLOG__",
         blog_entries
    ).replace(
        "__TEMPLATE_REPLACE_PERSONAL_PROJECTS__",
        projects
    ).replace(
        "__TEMPLATE_REPLACE_CERTIFICATIONS__",
        certs
    );


def build_personal_projects_list():
    ## Paths.
    url      = "https://api.github.com/users/N2OMatt/repos"
    response = urllib.urlopen(url);
    data     = json.loads(response.read());

    entries = "";
    for info in data:
        entries += "<li><b>{0}:</b> (<a href=\"{1}\">Github</a>)\n".format(
            info["name"],
            info["clone_url"]
        );

    return entries;

################################################################################
## Script                                                                     ##
################################################################################
## Clean up
os.system("rm    -rf ./_Output");
os.system("mkdir -p  ./_Output");

## Call the inner build scripts.
##   Blog
call_build_script       ("blog");
copy_build_script_output("blog");
##   Lectures
call_build_script       ("lectures");
copy_build_script_output("lectures");
##   Journal
call_build_script       ("journal");
copy_build_script_output("journal");
##   Resume
call_build_script       ("resume");
copy_build_script_output("resume");
##   Certifications
call_build_script       ("certifications");
copy_build_script_output("certifications");


index_template = read_file_text("index.template");
blog_entries   = read_file_text("_Output/blog/last_entries.txt");
projects       = build_personal_projects_list();
certifications = read_file_text("_Output/certifications/certs.html");

index_replaced = replace_index_template_contents(
    index_template,
    blog_entries,
    projects,
    certifications
);

write_file_text("_Output/index.html", index_replaced);