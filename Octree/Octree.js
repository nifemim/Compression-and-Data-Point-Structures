function newOctree(origin, halfDimension){
  var octree = new Object();
  octree.origin = origin;
  octree.halfDimension = halfDimension;
  octree.children = {1:null, 2:null, 3:null, 4:null, 5:null, 6:null, 7:null, 8:null};
  octree.dataPoint = null;

  return octree;
}

function vector3(x, y, z){
  var vector3 = new Object();
  vector3.x = x;
  vector3.y = y;
  vector3.z = z;

  return vector3;
}
function newOctreePoint(point){
  var octreePoint = new Object();
  octreePoint.position = point;

  return octreePoint;
}

function findOctant(octree, point){
  int octant = 0;
  if (point.x >= octree.origin.x) {
    oct |= 4;
  } if (point.y >= octree.origin.y) {
    oct |= 2;
  } if(point.z >= octree.origin.z) {
    oct |= 1;
  }

  return oct;
}

function isLeaf(octree) {
  if (octree.children[1] == null){
    return true;
  } else {
    return false;
  }
}

function insert(octree, point) {
  if (isLeaf(octree)) {
    if (octree.dataPoint == null) {
      octree.dataPoint = point;
      return;
    } else {
      var oldPoint = octree.dataPoint;
      octree.dataPoint = null;
      for (var i = 0; i<8; i++) {
        var newOrigin = octree.origin;
        newOrigin.x += halfDimension.x * (i&4 ? 0.5 : -0.5);
        newOrigin.y += halfDimension.y * (i&2 ? 0.5 : -0.5);
        newOrigin.z += halfDimension.z * (i&1 ? 0.5 : -0.5);
        octree.children[i] = newOctree(newOrigin, octree.halfDimension*0.5);
      }
      insert(octree.children[findOctant(oldPoint.position)], oldPoint);
      insert(octree.children[findOctant(point.position)], point);
    }
  } else {
    var octant = findOctant(point.position);
    insert(octree.children[octant], point);
  }
}

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
      cmax = octree.children[i].origin + octree.children[i].halfDimension;
      cmin = octree.children[i].origin - octree.children[i].halfDimension;

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