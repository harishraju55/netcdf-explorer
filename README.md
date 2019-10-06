# netcdf-explorer
This is a Desktop application to view NetCDF wrfout files (python + electron) that can be used on most of the operating systems.

Project motivation is to create a desktop application that can read netCDF files. And allow the user to choose a variable from the list of available variables from that file. 

Similar to the "NCVIEW" which is a widely used application to visualize the netCDF formatted files.

ncview: http://meteora.ucsd.edu/~pierce/ncview_home_page.html

### How to run

Please remember application is still in developement state.

* Make sure you have NodeJS and Python installed on your machine.

* Clone or download the project.

* Naviagte to the project directory (i.e /netcdf-explorer).

* Run commands: 
    * npm install
    * npm start

Use a sample netCDF wrfout file, You can find one here: https://www.ncl.ucar.edu/Applications/Data/


### Technology stack - Electron and Python

Electron is a non conventional framework to create desktop applications that can run on all operating systems.

### current working application screen shot.

![screenshot2](https://user-images.githubusercontent.com/9789209/59543009-b312a580-8ed6-11e9-820d-8896eb74f4d2.jpg)

Vertical Sounding feature.
![Uploading netcdf_explorer_capture2.jpg…]()

### To Do

* require cleanup and adjustments in CSS. currently referenced css from: https://mxb.dev/blog/css-grid-admin-dashboard/
* packaging issues, unable to generate python executables for the two python files.
* packaging is not accepting custom icon.

### Next

* Additional capabilities.
   * able to read different versions of netCDF files.
   * grib files.
 netcdf-explorer-v2
 netcdf-explorer-v2
