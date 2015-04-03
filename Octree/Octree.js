/**
 * This 'class' is my implementation of an octree. Below are functions for
 * different types of search and insertion.
 */


/**
 * This function instantiates a new octree with the given parameters.
 * @param {vector3} origin - the central origin point of this octree
 * @param {vector3} halfDimension - half the dimensions of this octree.
 * Represented as a 3 vector corresponding to half x, y, and z dimensiion. 
 * @return {Octree} octree
 */
function newOctree(origin, halfDimension){
  var octree = new Object();
  octree.origin = origin;
  octree.halfDimension = halfDimension;
  octree.children = {0: null, 1:null, 2:null, 3:null, 4:null, 5:null, 6:null, 7:null};
  octree.dataPoint = null;

  return octree;
}

/**
 * This function creates a vector3 object given the x,y,z coordinates
 * @param {Number} x
 * @param {Number} y
 * @param {Number} z
 * @return {vector3} vector3
 */
function vector3(x, y, z){
  var vector3 = new Object();
  vector3.x = x;
  vector3.y = y;
  vector3.z = z;

  return vector3;
}

function vector3Add(u, v) {
  return vector3(u.x+v.x, u.y+v.y, u.z+v.z);
}

function vector3Subtract(u, v) {
  return vector3(u.x-v.x, u.y-v.y, u.z-v.z); 
}
/**
 * This function creates an object that stores x,y,z coordinates in a single point
 * @param {vector3} point
 * @return {point} octreePoint
 */
function newOctreePoint(point){
  var octreePoint = new Object();
  octreePoint.position = point;

  return octreePoint;
}

/**
 * This function creates a vector3 object given the x,y,z coordinates
 * @param {Number} x
 * @param {Number} y
 * @param {Number} z
 * @return {vector3} vector3
 */
function findOctant(octree, point){
  var octant = 0;
  if (point.x >= octree.origin.x) {
    octant |= 4;
  } if (point.y >= octree.origin.y) {
    octant |= 2;
  } if(point.z >= octree.origin.z) {
    octant |= 1;
  }

  return octant;
}

/**
 * This function checks to see if the current octree is a leaf node or not. Since
 * a point can either have no children or all 8 (see insert below), we know that
 * if the first child element is empty, the tree must be empty.
 * @param {Octree} octree
 * @return {Boolean} true or false
 */
function isLeaf(octree) {
  if (octree.children[0] == null){
    return true;
  } else {
    return false;
  }
}

/**
 * This function return the current halfDimension of the octree divided by 2.
 * @param {Octree} octree
 * @return {vector3} toReturn
 */
function divideHalfDimension(octree){
  var toReturn = vector3(octree.halfDimension.x/2, octree.halfDimension.y/2, octree.halfDimension.z/2);
  return toReturn;
}

/**
 * This function sets the dataPoint of the given octree to the provided point.
 * @param {Octree} octree
 * @param {point} newPoint
 */
function setNewDataPoint(octree, newPoint) {
  octree.dataPoint = newPoint;
}

/**
 * This function inserts a point into the given octree
 * @param {Octree} octree
 * @param {point} point
 */
function insert(octree, point) {
  if (isLeaf(octree)) {
    if (octree.dataPoint == null) {
      setNewDataPoint(octree, point);
      return;
    } else {
      var oldPoint = octree.dataPoint;
      setNewDataPoint(octree, null);
      for (var i = 0; i<8; i++) {
        var newOrigin = octree.origin;
        newOrigin.x += octree.halfDimension.x * (i&4 ? 0.5 : -0.5);
        newOrigin.y += octree.halfDimension.y * (i&2 ? 0.5 : -0.5);
        newOrigin.z += octree.halfDimension.z * (i&1 ? 0.5 : -0.5);
        octree.children[i] = newOctree(newOrigin, divideHalfDimension(octree));
      }
      insert(octree.children[findOctant(octree, oldPoint.position)], oldPoint);
      insert(octree.children[findOctant(octree, point.position)], point);
    }
  } else {
    var octant = findOctant(octree, point.position);
    insert(octree.children[octant], point);
  }
}

/**
 * This function finds all the points stored in the octree within a 3-dimensional bounded box.
 * @param {Octree} octree
 * @param {vector3} min
 * @param {vector3} max
 * @param {point[]} results - the array that stores the found points
 */
function findInBoundedBox(octree, min, max, results){
  if (isLeaf(octree)) {
    if (octree.dataPoint!=null) {
      p = octree.dataPoint.position;
      if (p.x > max.x || p.y > max.y || p.z > max.z) {
        return;
      }
      if (p.x < min.x || p.y < min.y || p.z < min.z) {
        return;
      }
      results.push(octree.dataPoint);
    }
  } else {
    for (var i = 0; i < 8; i++) {
      cmax = vector3Add(octree.children[i].origin, octree.children[i].halfDimension);
      cmin = vector3Subtract(octree.children[i].origin, octree.children[i].halfDimension);

      if (cmax.x < min.x || cmax.y < min.y || cmax.z < min.z) {
        continue;
      }
      if (cmin.x > max.x || cmin.y > max.y || cmin.z > max.z) {
        continue;
      }
      findInBoundedBox(octree.children[i], min, max, results);
    }
  }
}

/**
 * Checks to see if two vectors are equal.
 * @param {vector3} u
 * @param {vector3} v
 * @return {boolean} true or false
 */
function vector3Equals(u, v) {
  if(u==null || v==null) {
    return false;
  }
  if (u.x != v.x || u.y != v.y || u.z != v.z) {
    return false;
  }
  return true;
}

/**
 * This function searches the octree for a location.
 * @param {octree} octree
 * @param {vector3} location
 * @return {octree}
 */
function octarySearch(octree, location) {
  if(octree.dataPoint != null && vector3Equals(octree.dataPoint.position, location)) {
    return octree;
  }
  
  if(isLeaf(octree)){
    return "Unable to find location within tree.";
  }

  var octant = findOctant(octree, location);
  if (vector3Equals(location, octree.children[octant].position)) {
    return octree.children[octant];
  }
  
  return octarySearch(octree.children[octant], location);
}