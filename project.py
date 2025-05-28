import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
import csv
import warnings
import threading
import time
import matplotlib.colors as mcolors
import matplotlib.cm as cm

#Function that calls all the other functions in this script
def functionCalls(fileName, fileNum, zoom_ans, zoom_amount): #This function is passed the file name and file variable of selected file
    time0 = time.time()
    #Changes file extension if the input file is not a TXT file
    if fileNum == 3:
        print("The selected file was a .txt file.") #Will also delete this later lol
        read_txt(fileName)
        #read_gac(fileName) #######This function only works for .gac files
    elif fileNum == 2:
        newFile = change_extension(fileName, 'txt')
        print("The selected file was a .gac file. ") #Print statement for checks only, will delete later
        #read_txt(newFile) ##############I think this function only works for .txt files
        csv_filename_gac = read_gac(newFile)
        radialSec = info_funct(newFile)
        gac_time_int_calc(csv_filename_gac, radialSec, zoom_ans, zoom_amount)
    elif fileNum == 1:
        print("The selected file was a .out file. ")
        newFile = change_extension(fileName, 'txt')
        read_out(newFile)
    else:
        print("The selected file was a .plum file. ")
        newFile = change_extension(fileName, 'txt')
        info_funct(newFile)
        read_plum(newFile)
    timef = time.time()
    totTime = timef - time0
    print(f"Total time to run: {totTime: 0.6f} seconds.")
        
#Function that reads data in a .txt file that was created by a previous run of this program
def read_txt(fileName):
    
    #Inform user that the .txt file is being read
    print("Reading .txt file.....")
    
    #Save .txt data into pandas DataFrame
    warnings.simplefilter("ignore")
    df = pd.read_csv(fileName, sep=r'\s+', index_col=False, engine = 'python', header = None)
    df = df[~df[0].astype(str).str.strip().str.startswith('*')] #This line gets rid of all commented lines in file
    df.reset_index(drop=True, inplace=True)
    df = df.map(lambda x: x.rstrip(',') if isinstance(x, str) else x) #Strips commas in file so csv will work better

    #Saves DataFrame to a .csv file for future reference
    df.to_csv(fileName[:-4] + '_' + fileName[-3:] + '.csv')
    
    #Informs user that the data was saved to a .csv file and to check .txt file for data details.
    print("File data has been saved to a .csv file. ")
    print("All comments in the original file have been deleted, please check created .txt file for data details.")
    
#This function changes the file extention to .txt
def change_extension(file_path, new_extension):
    
    #Informs user that file extension change is under way.
    print("Changing file extension to .txt file.....")
    
    #Change file extention
    base_name, og_ext = os.path.splitext(file_path)
    new_file_path = base_name + '_' + og_ext[1:] + "." + new_extension
    
    #Removes old text file if it exists
    try:
        shutil.copy(file_path, new_file_path)
    except:
        os.remove(new_file_path)
        change_extension(file_path, new_extension)
        
    #Informs user that the file extension was changed successfully
    print('File Extension Successfully Changed!')
    
    return new_file_path

#Function to truncate the datablocks into a csv
def read_gac(fileName):
    
    #Informs user about the process being done
    print('Cleaning GAC file, generating CSV...')

    #Open file to read, read file
    with open(fileName, "r") as f: 
        lines = f.readlines()

    #Create CSV file name, start writing to CSV
    csv_filename = f"{fileName[:-4]}_csv.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(["timestamp", "RadialRing", "AngularCompassDirection", "GroundConcentration", "TimeIntegratedAirConcentration", "AirConcentration"])

        #Iterate through txt file to separate data blocks
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            #This searches for the timestamp in the code
            if line.startswith("TIME"):
                timestamp = float(line.split(",")[1].strip())  # Extract timestamp
                i += 2  # Skip "BEGINDATABLOCK"

                #Keep reading the data for that timestamp until it reaches the end of the data block
                while not lines[i].strip().startswith("ENDDATABLOCK"):
                    values = [float(x) if "E" in x or "." in x else int(x) for x in lines[i].split(",")]
                    writer.writerow([timestamp] + values)
                    i += 1

            i += 1  # Move to next timestep or section

    #Tell user the data was saved to a csv
    print(f"Data saved to {csv_filename}")
    return csv_filename

#Function that informs user of important info stored in selected file.
def info_funct(fileName):
    print("Selected File Information: ")
    
    spaceEndpoints = pd.DataFrame(columns = ['Endpoint Distance', 'Endpoint Sector']) #Distances are in meters
            
    
    #Open file to read, read file
    with open(fileName, "r") as f: 
        lines = f.readlines()
        
    i = 0
    j = 1
    for i in range(len(lines)): ##Infinate loop rn lol
        line = lines[i].strip()
        #print('tessandra')
        #This searches for the important info in the file
        if line.startswith("LATITU"):
            latitude = float(line.split(",")[1].strip())  # Extract latitude
            print('Latitude: ' + str(latitude))
        elif line.startswith("LONGIT"):
            longitude = float(line.split(",")[1].strip())  # Extract longitude
            print('Longitude: ' + str(longitude))
        elif line.startswith("NUMRAD"):
            numOfSectors = int(line.split(",")[1].strip())  # Extract number of radial sectors
            print('Number of radial sectors: ' + str(numOfSectors))
        elif line.startswith("SPAEND"):
            spaceEndpoints.loc[j, 'Endpoint Distance'] = float(line.split(",")[1].strip())  # Extract and assign spacial endpoint distances   
            spaceEndpoints.loc[j, 'Endpoint Sector'] =  str(line.split(",")[0].strip()) #Extract and assign the endpoint number
            if j == (numOfSectors): #Only print the dataframe to the terminal once it is has all the data in it
                print(spaceEndpoints)
            j += 1
        elif line.startswith("NUMCOR"):
            compDir = int(line.split(",")[1].strip()) #Extracts and assigns the number of angular compass directions
            print("Number of angular compass directions: " + str(compDir))
        elif line.startswith("DATTIM"):
            month = int(line.split(",")[1].strip()) #Extract and assign month, day, hour, and second that the data was taken
            day = int(line.split(",")[2].strip())
            hour = int(line.split(",")[3].strip())
            sec = int(line.split(",")[4].strip())
            print("Month, day, hour, seconds: " + str(month) + ", " + str(day) + ", " + str(hour) + ", " + str(sec))
        elif line.startswith("ATDMODEL"):
            modelType = str(line.split(",")[1].strip()) #Extract and assign model type
            print("Model Type: " + modelType)
        elif line.startswith("NUCNAME"):
            nuclide = str(line.split(",")[1].strip())#Extract and assign nuclide name
            print("Nuclide Name: " + nuclide) 
        i += 1
    return compDir
    
#Function to read data from .plum file
def read_plum(fileName):
    
    #Inform user that program is reading the .plum file
    print("Reading .plum file.....")
    
    #Open file to read, read file
    with open(fileName, "r") as f: 
        lines = f.readlines()

    #Create CSV file name, start writing to CSV
    csv_filename = f"{fileName[:-4]}_csv.csv"
    
    #Initalize iterative variable
    k = 0
    
    #Open and create (if doesn't exist already) .csv file to write to
    with open(csv_filename, "w", newline="") as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(["PlumeSegment", "Direction", "Time", "LeadingEdgeDist", "TrailingEdgeDist", "LeadingEdgeWidth", "TrailingEdgeWidth"])

        # Iterate through txt file to separate data blocks
        while k < len(lines):
            line = lines[k].strip()

            # This searches for the plume segment in the code
            if line.startswith("BEGINPLMSEG"):
                plumseg = int(line.split(",")[1].strip())  # Extract plume segment
                k += 2  # Skip comment
                direction = int(line.split(",")[1].strip()) # Extract direction
                k += 2 # Skip comment
                
                # Keep reading the data for that timestamp until it reaches the end of the data block
                while not lines[k].strip().startswith("ENDDATABLOCK"):
                    values = [float(x) if "E" in x or "." in x else int(x) for x in lines[k].split(",")]
                    writer.writerow([plumseg] + [direction] + values) # Save values into same row in .csv
                    k += 1 # Go to next line

            k += 1  # Move to next line

    #Tell user the data was saved to a .csv
    print(f"Data saved to {csv_filename}")
    
    
#Function to read data from .out file
def read_out(fileName):
    print("Reading .out file.....")
    
    
#Function to make folders for figures and csvs if they don't exist
def makeFolders():
    
    #Define path to folder and folder name
    base_path = './'
    folder_name = 'Figure_Folder'

    #Combine base path and folder name to get the full path
    folder_path = os.path.join(base_path, folder_name)
    
    #Make folder if it doesn't exist yet
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    #Define path to folder and folder name
    base_path = './'
    folder_name = 'csv_Folder'

    #Combine base path and folder name to get the full path
    folder_path = os.path.join(base_path, folder_name)
    
    #Make folder if it doesn't exist yet
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

#Radial map of Cs-137 concentration (color-coded) after end of simulation (last data block)
    
def gac_time_int_calc(csv_filename, radialSec, zoom_ans, zoom_amount):
    print("Calculating total time integrated air concentration at end of simulation...")    
    
    fileName = csv_filename[-4:]
    
    gacdf = pd.read_csv(csv_filename)
    gacdf.to_csv('./gac.csv')
    
    #CSV column names: ["timestamp", "RadialRing", "AngularCompassDirection", "GroundConcentration", "TimeIntegratedAirConcentration", "AirConcentration"]
    
    #Inform user and make data frame
    print("Starting to make the wind rose ....")
    gacdf['TimeIntegratedAirConcentration'] = gacdf['TimeIntegratedAirConcentration']/ (10**12) ###Gets units from Bq to TBq for legend appearance.
    data = pd.DataFrame({'compasDir': gacdf['AngularCompassDirection'], 'timeIntAirConc': gacdf['TimeIntegratedAirConcentration']})
    
    #Ask user for direction and speed bins
    #num_direction_bins = int(radialSec)
    
    #Switching to gradient
    #num_conc_bins = 7 #Removed to move towards gradient
    
    # Define the direction and speed bins
    #direction_bins = np.linspace(0, 360, num_direction_bins + 1)
    #airConc_bins = np.linspace(0, data['timeIntAirConc'].max(), num_conc_bins + 1) #COmmented out to move to gradient

    ########################### ok up to here

    ################# Might need to do color gradient instead of distinct color bins

    # Bin the data manually
    # data['direction_bin'] = pd.cut(data['compasDir'], bins=direction_bins, labels=False, right=False)
    # #data['timeIntAirConcBin'] = pd.cut(data['timeIntAirConc'], bins=airConc_bins, labels=False, right=False) #Removed for gradient

    # # Create a pivot table to count occurrences in each bin
    # hist = data.pivot_table(index='direction_bin', columns='timeIntAirConc', aggfunc='size', fill_value=0)

    # print()
    # print(hist)
    # print()
    
    # column = hist['timeIntAirConc']
    # Compute the centers of the direction bins
    # direction_centers = (direction_bins[:-1] + direction_bins[1:]) / 2

    # # Normalize the histogram by the number of observations
    # hist_normalized = (hist / hist.sum().sum()) * 100

    # # Create the wind rose plot
    # fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111, polar=True)

    # # # Create a colormap for the bars
    # cmap = plt.cm.viridis
    # colors = cmap(np.linspace(0, 1, num_conc_bins))

    # #Initalize value
    # stacked_values = np.zeros(len(direction_centers))
    #color_norm = mcolors.Normalize(vmin=min(hist_normalized.loc[column]), vmax=max(hist_normalized.loc[column]))

    ############################################################################################################
    ############################################################################################################
    ############################################################################################################

    plt.figure(figsize=(10,10))
    bins = np.arange(0, 26, 1)
    plt.hist(data['compasDir'], bins = bins, edgecolor = 'black')
    plt.axis()
    plt.savefig('./Figure_Folder/TimeIntHistogram_' + fileName[:-4] + '.png')
    plt.show()

    # Sample data: wind directions (degrees) and speeds
    num_direction_bins = int(radialSec)
    dir_bins = np.linspace(0, 2*np.pi, num_direction_bins + 1) # Number of direction bins in rads.
    #wind_dir = dir_bins
    
    num_conc_bins = 8 #HARD CODED, can change later or make user set this param.
    cmap = plt.cm.viridis
    colors = cmap(np.linspace(0, 1, num_conc_bins))
    
    airConc_bins = np.linspace(0, data['timeIntAirConc'].max(), num_conc_bins + 1)
    #wind_speed = airConc_bins

    # Create histogram: counts of speeds per direction
    hist = np.zeros((len(dir_bins), len(airConc_bins) - 1))

   # Fill histogram
    for d, s in zip(dir_bins, airConc_bins):
        d_idx = int((d % 360) // 30)
        s_idx = np.searchsorted(airConc_bins, s, side='right') - 1
        if 0 <= s_idx < hist.shape[1]:
            hist[d_idx, s_idx] += 1

    # Normalize speed for colormap
    #norm = mcolors.Normalize(vmin=min(airConc_bins), vmax=max(airConc_bins))
    #cmap = cm.plasma  # Pick your favorite!

    # Set up polar plot
    fig, ax = plt.subplots(subplot_kw=dict(polar=True), figsize = (10,10))
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    # Bar width in radians
    bar_width = np.deg2rad(360/16)

    # Plot each data point individually
    # for k in range(num_direction_bins): #Replaced num_conc_bins with num_direction_bins
        
    #     values = hist_normalized.iloc[:, k].values
        
    #     ###################################################################### error here
        
    #     print(direction_centers)
    #     print()
    #     print(values)
    #     print()
        
    #     bar = ax.bar(np.deg2rad(direction_centers), values, bottom=stacked_values, 
    #                 width=np.deg2rad(360 / num_direction_bins), color=cmap(color_norm(values)), edgecolor='black', align='edge', alpha=0.7)
        
    #     #####################################################################
    
    #     # Update stacked_values to add the current values
    #     stacked_values += values
    
    # Plot
    for i, direction in enumerate(dir_bins):
        base = 0
        for j, count in enumerate(hist[i]):
            if count == 0:
                continue
            ax.bar(
                np.deg2rad(direction),
                count,
                width=bar_width,
                bottom=base,
                color=colors[j],
                edgecolor='black',
                linewidth=0.2
            )
            base += count

    # Create custom legend
    from matplotlib.patches import Patch
    legend_labels = [f"{airConc_bins[i]}–{airConc_bins[i+1]} Bq-s/m3" for i in range(len(airConc_bins) - 1)]
    patches = [Patch(facecolor=colors[i], edgecolor='black', label=legend_labels[i]) for i in range(len(colors))]
    plt.legend(handles=patches, bbox_to_anchor=(1.1, 1), loc='upper left', title="Time Integrated Air Concentration (1e12 magnitudes)")

    plt.title("Stacked Wind Rose with Predefined Colors")
    plt.tight_layout()
    plt.savefig('./Figure_Folder/TimeIntStackedWindrose_' + fileName[:-4] + '.png')
    plt.show()
    
    
    # for d, s in zip(dir_bins, airConc_bins):
    #     color = cmap(norm(s))
    #     ax.bar(
    #         np.deg2rad(d),     # angle
    #         s,                 # length
    #         width=bar_width,   # sector size
    #         color=color,
    #         edgecolor='black',
    #         linewidth=0.2,
    #         alpha=0.8
    #     )

    # # Add colorbar
    # sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    # sm.set_array([])
    # cbar = plt.colorbar(sm, ax=ax, pad=0.1)
    # cbar.set_label("Wind Speed (m/s)")

    # plt.title("Gradient Wind Rose")
    # plt.tight_layout()
    # plt.show()

    # Plot each bin as a bar in the wind rose
    # for k in range(num_direction_bins): #Replaced num_conc_bins with num_direction_bins
        
    #     values = hist_normalized.iloc[:, k].values
        
    #     ###################################################################### error here
        
    #     print(direction_centers)
    #     print()
    #     print(values)
    #     print()
        
    #     bar = ax.bar(np.deg2rad(direction_centers), values, bottom=stacked_values, 
    #                 width=np.deg2rad(360 / num_direction_bins), color=cmap(color_norm(values)), edgecolor='black', align='edge', alpha=0.7)
        
    #     #####################################################################
    
    #     # Update stacked_values to add the current values
    #     stacked_values += values
    
    #Add a legend
    # legend_labels = [f'{airConc_bins[i]:.1f} - {airConc_bins[i+1]:.1f} TBq-s/m^3' for i in range(num_conc_bins)] ##In Tera Bq units for key length
    # legend_handles = [plt.Line2D([0], [0], color=color, lw=10) for color in colors]
    # plt.legend(legend_handles, legend_labels, loc='upper right', bbox_to_anchor=(1.30, 1.0))

    #Finish procedure differently for zoom or non-zoom figures
    ans = zoom_ans
    
    #########################################################################Check if zoom in/out statements work lol
    
    #if/else statement for zoom implementation
#     if (ans == 2): # Means zoom in
        
#         #Add labels and title, set ylim
#         zoom = float(zoom_amount)
#         ax.set_theta_zero_location('N')
#         ax.set_theta_direction(-1)
#         y_ticks = np.linspace(0, int(zoom), num=5)
#         ax.set_yticks(y_ticks)
#         ax.set_yticklabels([f'{int(tick)}%' for tick in y_ticks])
#         ax.set_ylim(0, zoom)
#         warnings.simplefilter("ignore")
#         ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
#         ax.set_title('Zoomed Wind Rose ' + fileName, fontsize=16)
#         fig.savefig('./Zoomed_Wind_Rose_' + fileName[:-4] + '.png')
#         plt.show()
#         plt.close()
#         print('Wind rose complete! \n')
        
#     elif (ans == 1): # Means zoom out
        
#         #Add labels and title, set ylim
#         zoom = float(zoom_amount)
#         ax.set_theta_zero_location('N')
#         ax.set_theta_direction(-1)
#         y_ticks = np.linspace(0, int(zoom), num=5) 
#         ax.set_yticks(y_ticks)
#         ax.set_yticklabels([f'{int(tick)}%' for tick in y_ticks])
#         ax.set_ylim(0, zoom)
#         warnings.simplefilter("ignore")
#         ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
#         ax.set_title('Zoomed Wind Rose ' + fileName[:-4], fontsize=16)
#         fig.savefig('./Zoomed_Wind_Rose_' + fileName[:-4] + '.png')
#         plt.show()
#         plt.close()
#         print('Wind rose complete! \n')
# ############################################################################################Everything below should work        
#     elif (ans==0): # Means no zoom
        
#         #Add labels and title
#         ax.set_theta_zero_location('N')
#         ax.set_theta_direction(-1)
#         warnings.simplefilter("ignore")
#         ax.set_ylim(0, hist_normalized.max().max() + 1)
#         max_y = stacked_values.max() + 1
#         y_ticks = np.linspace(1, max_y, num=5)
#         ax.set_yticks(y_ticks)
#         ax.set_yticklabels([f'{int(tick)}%' for tick in y_ticks])
#         ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
#         ax.set_title('Wind Rose ' + fileName[:-4], fontsize=16)
#         fig.savefig('./Wind_Rose_' + fileName[:-4] + '.png')
#         plt.show()
#         plt.close()
#         print('Wind rose complete! \n')
     
    #Return direction and speed bins   
    return num_direction_bins, num_conc_bins
    
    
#Begins Python script
if __name__ == "__main__":
    functionCalls()
    
    