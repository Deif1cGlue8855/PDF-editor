import fitz
import os
import math

def splitPDF(path, save, cutPoints):   

    name = save    
    file_path = path 

    file = fitz.open(file_path)
    newFile = fitz.open()

    page = file[0]

    # Get page dimensions
    rect = page.rect
    print(f"Page dimensions: {rect}")

    print(f"Number of splits: {len(cutPoints)}")


    # Loop over the number of splits
    for i in range(len(cutPoints)):
        print(f"Processing split {i+1}")

        y0 = cutPoints[i]

        if(len(cutPoints) - i != 1):
            y1 = cutPoints[i+1]
        else:
            y1 = rect.height 

        # If the last part is smaller than the usual split size, adjust
        if y1 > rect.height:
            y1 = rect.height

        cBox = fitz.Rect(0, y0, rect.width, y1)  # Set the crop box for this part
        print(f"Cropping: {cBox}")

        # Apply the crop box to the page
        page.set_cropbox(cBox)
        
        # Create a new page in the new file with the desired dimensions
        newFile.new_page(width=rect.width, height=cBox.height)
        
        # Copy the cropped content onto the new page in the output PDF
        newFile[-1].show_pdf_page(fitz.Rect(0, 0, rect.width, cBox.height), file, 0)

    # Save the new file after processing all splits
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")    
    newFile.save(f"{downloads_path}/{name}.pdf")

    file.close()

    return ("File splice complete")
