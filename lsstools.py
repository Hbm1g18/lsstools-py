from dataclasses import dataclass, field
from typing import List

@dataclass
class Point:
    id: int
    x: float
    y: float
    z: float
    feature_code: str

@dataclass
class Link:
    feature_code: str
    points: List[Point] = field(default_factory=list)

def checkfileformat(file_path):
   """
    Checks to see if the input file is or isnt a recognised load file format.
    Currently supports .001-.009.
   """
   if not file_path.endswith(tuple(f".00{i}" for i in range(1,10))):
       raise ValueError("File is not a recognised load file format")

def read_data(file_path):
    """
    Reads data from file for use in other functions
    """
    checkfileformat(file_path)
    links = []
    points = []
    current_link = None
    current_feature_code = None

    with open(file_path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.startswith('21'):
                continue
            else: 
                parts = [part.strip() for part in line.split(',')]
                
                if len(parts) < 6:
                    continue
                
                data = {
                    'id': int(parts[1]),
                    'x': float(parts[2]),
                    'y': float(parts[3]),
                    'z': float(parts[4]),
                    'feature_code': parts[5]
                }
                
                if data['feature_code'].lower().startswith('p'):
                    points.append(Point(**data))
                    continue
                
                if data['feature_code'].startswith('.'):
                    data['feature_code'] = data['feature_code'][1:]
                    if current_link is not None:
                        links.append(current_link)
                    current_link = Link(data['feature_code'])
                    current_feature_code = data['feature_code']
                
                elif data['feature_code'] != current_feature_code:
                    if current_link is not None:
                        links.append(current_link)
                    current_link = Link(data['feature_code'])
                    current_feature_code = data['feature_code']
                
                point = Point(**data)
                current_link.points.append(point)

        if current_link is not None:
            links.append(current_link)

    return links, points


def featurecodes(file_path):
    """
    Returns a list of unique feature codes in load file.
    """
    links, points = read_data(file_path)
    link_features = {link.feature_code for link in links}
    point_features = {point.feature_code for point in points}
    unique_feature_codes = link_features.union(point_features)
    unique_feature_codes = sorted(list(unique_feature_codes))

    return unique_feature_codes

def boundingbox(file_path):
    """
    Return lower left and upper right bounding box based on survey data
    """
    links, points = read_data(file_path)
    min_x = float('inf')
    max_x = float('-inf')
    min_y = float('inf')
    max_y = float('-inf')
    for link in links:
        for point in link.points:
            if point.x < min_x:
                min_x = point.x
            if point.x > max_x:
                max_x = point.x
            if point.y < min_y:
                min_y = point.y
            if point.y > max_y:
                max_y = point.y
    for point in points:
        if point.x < min_x:
            min_x = point.x
        if point.x > max_x:
            max_x = point.x
        if point.y < min_y:
            min_y = point.y
        if point.y > max_y:
            max_y = point.y
    bbox = [min_x, min_y, max_x, max_y]
    return bbox

def z_info(file_path):
    """
    Return min, max and average z-values from file
    """
    z_values = []
    links, points = read_data(file_path)
    for link in links:
        for point in link.points:
            z_values.append(point.z)
    for point in points:
        z_values.append(point.z)
    z_values = sorted(z_values)
    min_z = z_values[0]
    max_z = z_values[-1]
    avg_z = sum(z_values) / len(z_values)
    return min_z, max_z, avg_z

def lssinfo(file_path):
    """
    Returns general information on load file provided.
    """
    bbox = boundingbox(file_path)
    min_z, max_z, avg_z = z_info(file_path)
    feature_codes = featurecodes(file_path)
    print(f"Bounding box for {file_path}:\n{bbox}")
    print(f"Z-value information:\nMin-z: {min_z}\nMax-z: {max_z}\nAvg-z: {avg_z}")
    print(f"Feature codes in {file_path}:\n{feature_codes}")

def querysurvey(file_path, feature_code):
    """
    Returns all links/points for feature code within filepath.
    """
    links, points = read_data(file_path)
    if feature_code.lower().startswith('p'):
       filtered_points = [point for point in points if point.feature_code.lower() == feature_code.lower()]
       return filtered_points
    else:
        filtered_links = [link for link in links if link.feature_code.lower() == feature_code.lower()]
        return filtered_links

def countfeature(file_path, feature_code):
    """
    Returns total number of links with feature code
    """
    return len(querysurvey(file_path, feature_code))

def feature_to_dxf(file_path, feature_code, output):
    """
    Generates point/polyline dxf of given featurecode whilst retaining 3D information.
    """
    feature = querysurvey(file_path, feature_code)
    if output.lower().endswith('.dxf'):
        output = output[:-4]
        file_name = f"{output}.dxf"
        with open(file_name, "w") as file:
            file.write("0\nSECTION\n2\nHEADER\n0\nENDSEC\n0\nSECTION\n2\nENTITIES\n")
            if isinstance(feature, list) and all(isinstance(item, Point) for item in feature):
                for point in feature:
                    file.write("0\nPOINT\n")
                    file.write(f"8\n{feature_code}\n")
                    file.write(f"10\n{point.x}\n")
                    file.write(f"20\n{point.y}\n")
                    file.write(f"30\n{point.z}\n")
            
            elif isinstance(feature, list) and all(isinstance(item, Link) for item in feature):
                for link in feature:
                    file.write("0\nPOLYLINE\n")
                    file.write("8\n{}\n".format(link.feature_code))
                    file.write("66\n1\n")
                    file.write("70\n8\n")
                    for point in link.points:
                        file.write("0\nVERTEX\n")
                        file.write(f"8\n{link.feature_code}\n")
                        file.write(f"10\n{point.x}\n")
                        file.write(f"20\n{point.y}\n")
                        file.write(f"30\n{point.z}\n")
                    file.write("0\nSEQEND\n")
            file.write("0\nENDSEC\n0\nEOF\n")
            file.close()
            print(f"Output saved as {file}")

def feature_to_geojson(file_path, feature_code, output):
    """
    Generates GeoJSON file for given feature code and stores 3D data as "elevation" property.
    """
    feature = querysurvey(file_path, feature_code)
    if output.lower().endswith('.geojson'):
        output = output[:-8]
    file_name = f"{output}.geojson"
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    if isinstance(feature, list) and all(isinstance(item, Point) for item in feature):
        for point in feature:
            feature_obj = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [point.x, point.y]
                },
                "properties": {
                    "elevation": point.z,
                    "feature_code": point.feature_code
                }
            }
            geojson["features"].append(feature_obj)
    
    elif isinstance(feature, list) and all(isinstance(item, Link) for item in feature):
        for link in feature:
            coordinates = [[point.x, point.y] for point in link.points]
            elevations = [point.z for point in link.points]
            if len(coordinates) > 1:
                feature_obj = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coordinates
                    },
                    "properties": {
                        "elevation": elevations,
                        "feature_code": link.feature_code
                    }
                }
                geojson["features"].append(feature_obj)
    with open(file_name, "w") as file:
        import json
        json.dump(geojson, file, indent=4)
    print(f"GeoJSON output saved as {file_name}")
