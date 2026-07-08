// =============================================================
// Dynamic Weather System — Neon rain, fog, lightning storms
// Tied to boss waves and game state
// =============================================================

import * as THREE from 'three';

export type WeatherType = 'clear' | 'neon_rain' | 'fog_pulse' | 'lightning_storm';

export interface WeatherState {
  type: WeatherType;
  intensity: number; // 0-1
  active: boolean;
  lightningTimer: number;
  nextLightningMs: number;
}

export class WeatherSystem {
  private scene: THREE.Scene;
  private rainParticles: THREE.Points | null = null;
  private rainGeometry: THREE.BufferGeometry | null = null;
  private rainMaterial: THREE.PointsMaterial | null = null;
  private fogDensity: number = 0;
  private ambientLight: THREE.AmbientLight | null = null;
  private lightningLight: THREE.PointLight | null = null;
  
  private state: WeatherState = {
    type: 'clear',
    intensity: 0,
    active: false,
    lightningTimer: 0,
    nextLightningMs: 30000,
  };

  constructor(scene: THREE.Scene) {
    this.scene = scene;
    
    // Setup ambient light for weather
    this.ambientLight = new THREE.AmbientLight(0x404060, 0.3);
    this.scene.add(this.ambientLight);
    
    // Lightning flash light (initially off)
    this.lightningLight = new THREE.PointLight(0xaaddff, 0, 100);
    this.lightningLight.position.set(0, 50, 0);
    this.scene.add(this.lightningLight);
  }

  setWeather(type: WeatherType, intensity: number = 1): void {
    this.state.type = type;
    this.state.intensity = Math.max(0, Math.min(1, intensity));
    this.state.active = intensity > 0;
    
    switch (type) {
      case 'clear':
        this.clearWeather();
        break;
      case 'neon_rain':
        this.setupNeonRain(intensity);
        break;
      case 'fog_pulse':
        this.setupFogPulse(intensity);
        break;
      case 'lightning_storm':
        this.setupLightningStorm(intensity);
        break;
    }
  }

  private clearWeather(): void {
    if (this.rainParticles) {
      this.scene.remove(this.rainParticles);
      this.rainParticles = null;
    }
    if (this.rainGeometry) {
      this.rainGeometry.dispose();
      this.rainGeometry = null;
    }
    if (this.rainMaterial) {
      this.rainMaterial.dispose();
      this.rainMaterial = null;
    }
    this.fogDensity = 0;
    this.scene.fog = null;
    if (this.lightningLight) {
      this.lightningLight.intensity = 0;
    }
  }

  private setupNeonRain(intensity: number): void {
    const particleCount = Math.floor(1500 * intensity);
    
    if (!this.rainGeometry) {
      this.rainGeometry = new THREE.BufferGeometry();
      const positions = new Float32Array(particleCount * 3);
      const velocities = new Float32Array(particleCount);
      
      for (let i = 0; i < particleCount; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 100;     // x
        positions[i * 3 + 1] = Math.random() * 50;           // y
        positions[i * 3 + 2] = (Math.random() - 0.5) * 100;  // z
        velocities[i] = 20 + Math.random() * 10;
      }
      
      this.rainGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      this.rainGeometry.setAttribute('velocity', new THREE.BufferAttribute(velocities, 1));
    }
    
    if (!this.rainMaterial) {
      this.rainMaterial = new THREE.PointsMaterial({
        color: 0x00ffff,
        size: 0.15,
        transparent: true,
        opacity: 0.6 * intensity,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      });
    }
    
    if (!this.rainParticles) {
      this.rainParticles = new THREE.Points(this.rainGeometry, this.rainMaterial);
      this.scene.add(this.rainParticles);
    }
    
    // Add subtle cyan fog
    this.fogDensity = 0.02 * intensity;
    this.scene.fog = new THREE.FogExp2(0x050510, this.fogDensity);
  }

  private setupFogPulse(intensity: number): void {
    this.fogDensity = 0.03 * intensity;
    this.scene.fog = new THREE.FogExp2(0x1a0a2e, this.fogDensity);
  }

  private setupLightningStorm(intensity: number): void {
    this.setupNeonRain(intensity * 0.8);
    this.setupFogPulse(intensity * 1.2);
    this.state.nextLightningMs = 3000 + Math.random() * 5000;
    this.state.lightningTimer = 0;
  }

  update(deltaTime: number, gameTime: number): void {
    // Update rain particles
    if (this.rainParticles && this.rainGeometry) {
      const positions = this.rainGeometry.getAttribute('position') as THREE.BufferAttribute;
      const velocities = this.rainGeometry.getAttribute('velocity') as THREE.BufferAttribute;
      
      for (let i = 0; i < positions.count; i++) {
        const y = positions.getY(i);
        const vel = velocities.getX(i);
        
        // Move rain down
        positions.setY(i, y - vel * deltaTime);
        
        // Reset when hits ground
        if (y < 0) {
          positions.setY(i, 50);
          positions.setX(i, (Math.random() - 0.5) * 100);
          positions.setZ(i, (Math.random() - 0.5) * 100);
        }
      }
      
      positions.needsUpdate = true;
    }
    
    // Pulse fog density
    if (this.state.type === 'fog_pulse' || this.state.type === 'lightning_storm') {
      const pulse = Math.sin(gameTime * 0.5) * 0.3 + 0.7;
      const baseDensity = this.state.type === 'lightning_storm' ? 0.03 : 0.02;
      this.fogDensity = baseDensity * this.state.intensity * pulse;
      if (this.scene.fog) {
        this.scene.fog.density = this.fogDensity;
      }
    }
    
    // Lightning flashes
    if (this.state.type === 'lightning_storm' && this.lightningLight) {
      this.state.lightningTimer += deltaTime * 1000;
      
      if (this.state.lightningTimer >= this.state.nextLightningMs) {
        this.triggerLightning();
        this.state.lightningTimer = 0;
        this.state.nextLightningMs = 2000 + Math.random() * 6000;
      }
      
      // Fade out lightning
      if (this.lightningLight.intensity > 0) {
        this.lightningLight.intensity = Math.max(0, this.lightningLight.intensity - deltaTime * 10);
      }
    }
  }

  private triggerLightning(): void {
    if (this.lightningLight) {
      this.lightningLight.intensity = 5 + Math.random() * 3;
      this.lightningLight.color.setHex(Math.random() > 0.5 ? 0xaaddff : 0xffaaee);
      
      // Flash entire scene briefly
      if (this.ambientLight) {
        const originalIntensity = 0.3;
        this.ambientLight.intensity = 0.8;
        setTimeout(() => {
          if (this.ambientLight) {
            this.ambientLight.intensity = originalIntensity;
          }
        }, 100);
      }
    }
  }

  getWeatherState(): WeatherState {
    return { ...this.state };
  }

  dispose(): void {
    this.clearWeather();
    if (this.ambientLight) {
      this.scene.remove(this.ambientLight);
      this.ambientLight = null;
    }
    if (this.lightningLight) {
      this.scene.remove(this.lightningLight);
      this.lightningLight = null;
    }
  }
}
