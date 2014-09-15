from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os, sys
import subprocess

'''
Usage: python map-in-picture.py photo1.JPG photo2.JPG
Set variable maperitive_path to maperitive.exe!

'''

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data

def _get_if_exist(data, key):
    if key in data:
        return data[key]
		
    return None
	
def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:		
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":                     
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def gen_maps(data, map_w, map_h):
    maperitive_path='D:\Programs\_Maps\Maperitive\Maperitive.exe'
    lat = data[0]
    lon = data[1]
    f = open('temp.mscript', 'w')
    f.write('clear-map\n')
    #f.write('add-web-map provider="hikebike"\n')
    f.write('load-source data.osm\n')
    f.write('use-ruleset alias="ad47"\n')
    f.write('load-source "'+os.getcwd()+'\\maps\\temp.gpx"\n')    
    
    f.write('clear-map\n')
    #f.write('add-web-map provider="hikebike"\n')
    f.write('add-web-map provider="mapquest.osm"\n')
    #f.write('load-source data.osm\n')
    f.write('use-ruleset alias="ad47"\n')
    f.write('load-source "'+os.getcwd()+'\\maps\\temp.gpx"\n')
    
    f.write('move-pos x='+str(lon)+' y='+str(lat)+' zoom=10\n')
    f.write('set-setting name="map.decoration.attribution" value="False"\n')
    f.write('pause\n')
    f.write('export-bitmap width='+str(map_w)+' height='+str(map_h)+' zoom=10 file=maps/1.png\n')
    f.write('export-bitmap width='+str(map_w)+' height='+str(map_h)+' zoom=14 file=maps/2.png\n')
    f.write('export-bitmap width='+str(map_w)+' height='+str(map_h)+' zoom=16 file=maps/3.png\n')
    f.close()
    
    os.system(maperitive_path+'  -exitafter '+os.getcwd()+'/temp.mscript')#
		
    return None	

def gen_point_gpx(data):  
    f = open('maps/temp.gpx', 'w')
    lat = data[0]
    lon = data[1]
    text='''<?xml version='1.0' encoding='UTF-8'?>
<gpx version="1.1" creator="Small python script" xmlns="http://www.topografix.com/GPX/1/1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
  </metadata>
  '''
    f.write(text)
    f.write('  <wpt lat="'+str(lat)+'" lon="'+str(lon)+'"/>')
    f.write('</gpx>')
    f.close()
    



 
################
# Example ######
################
if __name__ == "__main__":

    print "Usage: python map-in-picture.py d:\upload\2014-08\2\_20140817_227.JPG d:\upload\2014-08\2\_20140817_237.JPG"
	
    size = 128, 128

    for infile in sys.argv[1:]:
        outfile = os.path.splitext(infile)[0] + ".new.jpg"
        print infile
        if infile != outfile:
            try:
                filename = infile
                image = Image.open(filename)
                exif_data = get_exif_data(image)
                print 'Photo coords founded'
                gen_point_gpx(get_lat_lon(exif_data))

                im = Image.open(infile) #
                im.thumbnail(size)      #
                
                source_width, source_height = image.size
                
			
            
                target_h=768
                target_h=source_height
                map_border_h=1
                map_border_v=1

                
                map_w=340
                map_w = (source_width-(2*map_border_v))//3
                map_h=250
                #if source_width-source_height>200: 
                #    map_h=source_width-source_height-map_border_h-map_border_h
                
                gen_maps(get_lat_lon(exif_data),map_w,map_h)
                
                
                
                white=(0,0,0)
                
                #new canvas size
                #isize=(1024,target_h+map_h+map_border_v+map_border_v)
                isize=(source_width,target_h+map_h+map_border_v+map_border_v)
                
                print isize   
                inew = Image.new('RGB',isize,white)
                imgsrc = Image.open(infile)
                inew.paste(imgsrc,(0,0,source_width,source_height))


                left = 0
                right = map_w
                upper = target_h+map_border_v
                lower = target_h+map_h+map_border_v
                bbox = (left,upper,right,lower)
                imgmap = Image.open('maps/1.png')
                inew.paste(imgmap,bbox)
			
                left = map_w+(map_border_h*1)
                right = left+map_w
                upper = target_h+map_border_v
                lower = target_h+map_h+map_border_v
                bbox = (left,upper,right,lower)
                imgmap = Image.open('maps/2.png')
                inew.paste(imgmap,bbox)	
			
                left = (map_w*2)+(map_border_h*2)
                right = left+map_w
                upper = target_h+map_border_v
                lower = target_h+map_h+map_border_v
                bbox = (left,upper,right,lower)
                imgmap = Image.open('maps/3.png')
                inew.paste(imgmap,bbox)
			
            
                exif = imgsrc.info['exif']  
                inew.save(outfile, quality=95)
                subprocess.call(['exiftool.exe',
                                 outfile,
                                 '-tagsFromFile',
                                 filename], shell=True)

            except IOError:
                print "cannot create thumbnail for", infile
