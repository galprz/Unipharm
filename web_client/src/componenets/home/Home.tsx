import React from 'react'
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import Utils from "./HomeUtils";
import Button from '@material-ui/core/Button';
import "./HomeStyle.css";
import consts from "./HomeConsts.json";

class WarehouseScene extends React.Component {
  mount: any;
  scene!: THREE.Scene;
  renderer!: THREE.WebGLRenderer;
  camera!: THREE.PerspectiveCamera;
  controls!: OrbitControls;
  cubes: Array<THREE.Mesh<THREE.BoxGeometry, THREE.MeshBasicMaterial>> = [];
  freedomMesh: any;
  frameId: any;
  loader: any;
  forklift: any;
  direction: number = consts.forklift.direction.still;
  videoStarted: boolean = false;
  geometry = new THREE.BoxGeometry(consts.boxEdge, consts.boxEdge, consts.boxEdge);
  green = new THREE.MeshBasicMaterial({
    color: "#0F0"
  });
  red = new THREE.MeshBasicMaterial({
        color: "#F00"
  });
  white = new THREE.MeshBasicMaterial({
    color: "#FFF"
  });
  paused: any;
  ended: any;
  createMaterialArray() {
    var skyboxImagepaths : Array<string>= ["/px.png", "/nx.png", 
    "/py.png", "/ny.png", "/pz.png", "/nz.png"];
    var materialArray = skyboxImagepaths.map(image => {
      var texture = new THREE.TextureLoader().load(image);
  
      return new THREE.MeshBasicMaterial({ map: texture, side: THREE.BackSide });
    });
    return materialArray;
  }
  componentDidMount() {
    this.scene = new THREE.Scene();

    var skyboxGeo = new THREE.BoxGeometry(consts.skyboxEdge, consts.skyboxEdge, consts.skyboxEdge);
    var skybox = new THREE.Mesh(skyboxGeo, this.createMaterialArray());
    this.scene.add(skybox);

    //Add Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setClearColor("#FFFFFF");
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.mount.appendChild(this.renderer.domElement);

    //add Camera
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 45, 30000);
    var cameraPosition = consts.camera.position
    this.camera.position.set(cameraPosition.x, cameraPosition.y, cameraPosition.z);

    //Camera Controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.enableZoom = true;
    this.controls.dampingFactor = 0.25;
    this.controls.update();

    //LIGHTS
    for(var i = 0; i < consts.lights.length; i++)
    {
      var light = new THREE.PointLight(0xffffff, 1, 0);
      var lightPosition = consts.lights[i];
      light.position.set(lightPosition.x, lightPosition.y, lightPosition.z);
      this.scene.add(light);
    }

    this.addModels();

    this.renderer.render(this.scene, this.camera);

    //start animation
    this.start();
  }

  onClick(myThis: any){
      if(!(myThis.direction === consts.forklift.direction.still)) //We started moving already
      {
        myThis.direction *= -1;
        myThis.forklift.rotation.y += Math.PI;
      }
      else //First time moving
      {
        myThis.direction = consts.forklift.direction.backwards;
      }
      this.videoStarted = true;
  }

  addModels() {
    // -----Step 1--------
    var locations = Utils.getLocations();

    for(var i = 0; i < locations.length; i++){
            var mesh : THREE.Mesh<THREE.BoxGeometry, THREE.MeshBasicMaterial>;
            mesh = new THREE.Mesh(this.geometry, this.white);
            mesh = new THREE.Mesh(this.geometry, this.white);
            mesh.position.set(locations[i][0], locations[i][1], locations[i][2]);
            this.scene.add(mesh);
            this.cubes.push(mesh);
            //console.log(locations[i][0] + " " + locations[i][1] + " " + locations[i][2]);
    };

    // -----Step 2--------
    //LOAD TEXTURE and on compvarion apply it on SPHERE
    this.loader = new THREE.TextureLoader().load(
      "https://media.licdn.com/dms/image/C4E0BAQH1TBGFHZF_GQ/company-logo_200_200/0?e=2159024400&v=beta&t=TNdhRWq0i8sG4cA9QERCfF8fSsF_zrMZNSQD-pK5YO8",
      texture => {
        //Update Texture
        this.cubes.forEach(function (cube) {
          cube.material.map = texture;
          cube.material.needsUpdate = true;
        }); 
      }
    );

    var geometry = new THREE.PlaneGeometry( 5, 10, 32 );
    var material = new THREE.MeshBasicMaterial( {color: 0x000000, side: THREE.DoubleSide} );
    var yOffset = 3;
    for(var j = 0; j < locations.length; j++){
      var plane = new THREE.Mesh( geometry, material );
      plane.position.set(locations[j][0], locations[j][1] - yOffset, locations[j][2]);
      plane.rotation.x = Math.PI / 2;
      plane.rotation.z = Math.PI / 2;
      this.scene.add( plane );
    }

    var height = consts.warehouse.height;
    var width = consts.warehouse.width;
    var sideGeometry = new THREE.PlaneGeometry(width, height);
    var backGeometry = new THREE.PlaneGeometry(height, height);
    var floorTexture = new THREE.TextureLoader().load("/wall.jfif");
    var sideTexture = new THREE.TextureLoader().load("/wall_logo.png");
    var floorMaterial = new THREE.MeshBasicMaterial( { map: floorTexture, side: THREE.DoubleSide } );
    var sideMaterial = new THREE.MeshBasicMaterial( { map: sideTexture, side: THREE.DoubleSide } );
    var floor = new THREE.Mesh(sideGeometry, floorMaterial);
    var warehousePosition = consts.warehouse.position;
    floor.position.set(warehousePosition.x, warehousePosition.y, warehousePosition.z);
    floor.rotation.x = Math.PI / 2;
    this.scene.add( floor );
    var ceiling = new THREE.Mesh(sideGeometry, floorMaterial);
    ceiling.position.set(warehousePosition.x, warehousePosition.y + height, warehousePosition.z);
    ceiling.rotation.x = Math.PI / 2;
    this.scene.add( ceiling );
    var back = new THREE.Mesh(backGeometry, sideMaterial);
    back.position.set(warehousePosition.x - width/2, warehousePosition.y + height/2, warehousePosition.z);
    back.rotation.y = - Math.PI / 2;
    this.scene.add( back );
    var side1 = new THREE.Mesh(sideGeometry, sideMaterial);
    side1.position.set(warehousePosition.x, warehousePosition.y + height/2, warehousePosition.z + height/2);
    this.scene.add( side1 );
    var side2 = new THREE.Mesh(sideGeometry, sideMaterial);
    side2.position.set(warehousePosition.x, warehousePosition.y + height/2, warehousePosition.z - height/2);
    side2.rotation.y = Math.PI;
    this.scene.add( side2 );

    this.forklift = new THREE.Object3D();
    this.scene.add(this.forklift);

    var objLoader = new OBJLoader();
    objLoader.load(
      // resource URL
      "/Forklift.obj",
    
      // onLoad callback
      // Here the loaded data is assumed to be an object
       ( obj ) => {
        // Add the loaded object to the scene
        var forkliftPosition = consts.forklift.position;
        this.forklift.position.set(forkliftPosition.x, forkliftPosition.y, forkliftPosition.z);
        this.forklift.scale.multiplyScalar(consts.forklift.sizeMultiplyer);
        this.forklift.model = obj;
        this.forklift.add(this.forklift.model);
      }
    );
  }

  loadCubeTexture(cubeIndex: number, material: THREE.MeshBasicMaterial)
  {
    this.cubes[cubeIndex].material = material;
    this.cubes[cubeIndex].material.needsUpdate = true;
    this.loader = new THREE.TextureLoader().load(
      "https://media.licdn.com/dms/image/C4E0BAQH1TBGFHZF_GQ/company-logo_200_200/0?e=2159024400&v=beta&t=TNdhRWq0i8sG4cA9QERCfF8fSsF_zrMZNSQD-pK5YO8",
      (        texture: THREE.Texture | null) => {
        //Update Texture
        this.cubes[cubeIndex].material.map = texture;
        this.cubes[cubeIndex].material.needsUpdate = true;
      });
  }

  componentWillUnmount() {
    this.stop();
    this.mount.removeChild(this.renderer.domElement);
  }
  start = () => {
    if (!this.frameId) {
      this.frameId = requestAnimationFrame(this.animate);
    }
  };
  stop = () => {
    cancelAnimationFrame(this.frameId);
  };
  animate = () => {
    if (this.freedomMesh) this.freedomMesh.rotation.y += 0.01;
    this.forklift.position.x += consts.forklift.speed * this.direction;
    if(this.forklift.position.x < -150 || this.forklift.position.x > 23)
    {
      this.forklift.rotation.y += Math.PI;
      this.direction *= -1;
    }
    if(this.videoStarted)
    {
      var vid = document.getElementById("demoVideo") as HTMLVideoElement;
      vid.play();
      this.videoStarted = true;
    }
    var prevGreen = false;
    var xDistance = 10;
    for(var i = 0; i > -140; i -= xDistance)
    {
      if(this.forklift.position.x < i)
      {
          var color = Utils.getColor(840 + 6*i);
          if(prevGreen)
          {
            this.loadCubeTexture(840 + 6*(i + xDistance), this.white);
          }
          if(color === 0)
          {
            this.loadCubeTexture(840 + 6*i, this.green);
            prevGreen = true;
          }
          else
          {
            this.loadCubeTexture(840 + 6*i, this.red);
            prevGreen = false;
          }
      }
    }
    if(this.forklift.position.x < -140)
    {
      this.direction = consts.forklift.direction.still;
    }
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
    this.frameId = window.requestAnimationFrame(this.animate);
  };

  render() {
    return (
      <div>
        <Button onClick={() => this.onClick(this)} variant="contained" color='primary' className="ontop">Start</Button>
        <video width="480" height="360" className="ontop" id="demoVideo">
          <source src="/Demo.mp4" type="video/mp4"></source>
        </video>
        <div
          style={{ width: "800px", height: "600px" }}
          ref={mount => {
            this.mount = mount;
          }}
        />
      </div>
    );
  }
}

export default WarehouseScene;