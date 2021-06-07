# picren
Picren helps you rename and reorganise your photos by date and location.\
Simply provide a valid folder or photo that you'd like to convert and a valid folder to place and create your very own picren-ified library.

### Current (and default) functionality 
  **Organisation**:
  * Photos are moved to the destination folder and placed in a hierarchical order based on the address from the top down.
  * Full structure provided below
    
  **Naming**:
  * Photos will be renamed (in this order) to the date, time and location (if present) 
    when/where the photo was taken.
    
  **Picren Library Directory Structure**: 
  
  > Picren

 >> Country

 >>> State

 >>>> Suburb

 >>>>> date_time_village.JPG

 >>> City

 >>>> date_time_suburb.JPG

 >> __No Location__

 >>> Year

 >>>> date_time.JPG

 >>> __No Date__

 >>>> original_name.JPG

### To use picren, you'll need
+ Exiftool
   > [Download link for macOS](https://exiftool.org/ExifTool-12.26.dmg)
 
   > If you're already using homebrew, simply install exiftool with `brew install exiftool`
+ A stable internet connection

### Installation Guide
+ Download the latest release .zip file
+ Right click on the picren folder, go down to 'Services' and select 'New terminal at Folder' 
+ On your terminal window and type `mv picren /usr/local/bin`
+ Now type in `picren` and voila, you can now use the app!
+ To run picren in the future, simply open up your preferred terminal application and just type `picren`, it's that easy.
