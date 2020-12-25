import React from 'react'
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
import Utils from "./HomeUtils";
import Button from '@material-ui/core/Button';
import "./HomeStyle.css";

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
  direction: number = 0;
  videoStarted: boolean = false;
  geometry = new THREE.BoxGeometry(5, 5, 5);
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

    var skyboxGeo = new THREE.BoxGeometry(10000, 10000, 10000);
    var skybox = new THREE.Mesh(skyboxGeo, this.createMaterialArray());
    this.scene.add(skybox);

    //Add Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setClearColor("#FFFFFF");
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.mount.appendChild(this.renderer.domElement);

    //add Camera
    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 45, 30000);
    this.camera.position.set(58, 45, 30);

    //Camera Controls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.enableZoom = true;
    this.controls.dampingFactor = 0.25;
    this.controls.update();

    //LIGHTS
    var lights = [];
    lights[0] = new THREE.PointLight(0x304ffe, 1, 0);
    lights[1] = new THREE.PointLight(0xffffff, 1, 0);
    lights[2] = new THREE.PointLight(0xffffff, 1, 0);
    lights[0].position.set(0, 200, 0);
    lights[1].position.set(100, 200, 100);
    lights[2].position.set(-100, -200, -100);
    this.scene.add(lights[0]);
    this.scene.add(lights[1]);
    this.scene.add(lights[2]);

    this.addModels();

    this.renderer.render(this.scene, this.camera);

    //start animation
    this.start();
  }

  onClick(myThis: any){
      if(!(myThis.direction === 0)) //We started moving already
      {
        myThis.direction *= -1;
        myThis.forklift.rotation.y += Math.PI;
      }
      else //First time moving
      {
        myThis.direction = -1;
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

    var floorGeometry = new THREE.PlaneGeometry( 150, 250, 32 );
    var floorGeometry2 = new THREE.PlaneGeometry( 150, 154, 32 );
    var floorGeometry3 = new THREE.PlaneGeometry( 154, 250, 32 );
    var floorTexture = new THREE.TextureLoader().load("/wall.jfif");
    var floorTexture2 = new THREE.TextureLoader().load("/wall_logo.png");
    var floorTexture3 = new THREE.TextureLoader().load("/wall_logo_rotate.png");
    var floorMaterial = new THREE.MeshBasicMaterial( { map: floorTexture, side: THREE.DoubleSide } );
    var floorMaterial2 = new THREE.MeshBasicMaterial( { map: floorTexture2, side: THREE.DoubleSide } );
    var floorMaterial3 = new THREE.MeshBasicMaterial( { map: floorTexture3, side: THREE.DoubleSide } );
    var floor = new THREE.Mesh( floorGeometry, floorMaterial );
    floor.position.set(-35, -3, 30);
    floor.rotation.x = Math.PI / 2;
    floor.rotation.z = Math.PI / 2;
    this.scene.add( floor );
    var floor2 = new THREE.Mesh( floorGeometry, floorMaterial );
    floor2.position.set(-35, 151, 30);
    floor2.rotation.x = Math.PI / 2;
    floor2.rotation.z = Math.PI / 2;
    this.scene.add( floor2 );
    var floor3 = new THREE.Mesh( floorGeometry2, floorMaterial2);
    floor3.position.set(-160, 74, 30);
    floor3.rotation.y = - Math.PI / 2;
    this.scene.add( floor3 );
    var floor4 = new THREE.Mesh( floorGeometry3, floorMaterial3 );
    floor4.position.set(-35, 74, 105);
    floor4.rotation.z = Math.PI / 2;
    this.scene.add( floor4 );
    var floor5 = new THREE.Mesh( floorGeometry3, floorMaterial3 );
    floor5.position.set(-35, 74, -45);
    floor5.rotation.z = Math.PI / 2;
    floor5.rotation.y = Math.PI;
    this.scene.add( floor5 );

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
        this.forklift.scale.multiplyScalar(0.03);
        this.forklift.position.set(23, -2, 13);
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
    this.forklift.position.x += 0.06 * this.direction;
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
      this.direction = 0;
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