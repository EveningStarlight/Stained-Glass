# Stained-Glass
This project seeks to create images resembling stained glass from photos

## Stained Glass Image Filter

Adam Prins, 100 879 683

## Summary
This project seeks to create images resembling stained glass using photos. It will determine important features, and how best to represent them using simple geometries. I will include some user controls for manipulating the transformation settings.

## Background
I have previously developed a program for randomly generated triangles for image generation, and noticed that it had a nice effect for images, shown in figure 1. Since the points were generated randomly, a large number of them were required to provide recognizable images.

![A mosaic of a bird made using 1000 points. The large details of the bird can be made out, but are not particularly sharp or vivid.](/docs/images/bird-1000-points.png)
Figure 1 Mosaic of a bird generated with 1000 points


## Challenge
The challenges to this project will be determining which regions will be represented in the transformation (smaller features may be ignored if the user highly constrains the transformation), creating geometries to match the ranked regions, and performing transformations with specified user settings.

An image like in Figure 1 should be created using closer to 50 geometries that have better detailing.

## Results

The application has a simple to use GUI, and is accessible to almost all users. It consists of a tab of options for changing the groupings and how they are displayed, and a tab for the colours and how they are represented.

![An image displaying A processed picture of some mountains on the left, and a settings console on the right](/docs/images/example_1-GUI.png)
Figure 2 - The GUI
 
The application can be used to create many interesting images.

![On the left is a picture of two brightly coloured drinks on a table, 
on the right is an abstracted version](/docs/images/example_2-Processing.png)
 Figure 3 - Standard Colours
 
 ![On the left is a picture of a boat just off the coast, 
 on the right is a version where all the blues are now orange, and the boat has gone from white to bright green](/docs/images/example_3-Pop.jpg)
 Figure 4 - Pop Colours
 
 ![On the left is a picute of a bird, 
 and on the right is an abstracted image that shows the general outline and features of the bird. All the colours in the right image are random](/docs/images/example_4-Random.jpg)
 Figure 5 - Random Colours

The application also uses a cache, so while processing new configurations may take a few seconds, switching back to previously used ones is instant.
The image is processed at its native resolution, even though the UI displays it as a square. So when you save the results of the application, the output is correctly done at the native resolution.

## Goals and Deliverables
The primary goals for the project will be:
* determining coloured regions
* rank the regions using a priority measure
* create geometries for top N regions
* output a new image based on the above

The secondary goals are:
* Having user controls for manipulating
  * number of N regions
  * the ranking of regions
  * the possible geometries

## Schedule
The tentative schedule is as follows:
* February 8th
  * select libraries
  * import/export images
* February 15th
  * build framework GUI
* February 22nd
  * refine GUI
* March 1st
  * determine coloured regions
  * rank regions using simple heuristics
* March 8th
  * Map geometries to regions
  * select representative colours for regions
* March 15th
  * add additional user controls
* March 22nd
  * buffer week for unplanned delays
* March 29th
  * beautify image
* April 5th
  * complete final project paper
* April 12th
  * review final project paper
