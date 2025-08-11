// Mock DockerServiceClient to allow service-dashboard.html to function without a real backend

class DockerServiceClient {
    constructor(config) {
        this.config = config;
        this.eventListeners = new Map();
        this.mockServices = this.generateMockServices();

        // Simulate initial data load
        setTimeout(() => this.emit('services-updated', this.mockServices), 500);
    }

    on(eventName, callback) {
        if (!this.eventListeners.has(eventName)) {
            this.eventListeners.set(eventName, []);
        }
        this.eventListeners.get(eventName).push(callback);
    }

    emit(eventName, data) {
        if (this.eventListeners.has(eventName)) {
            this.eventListeners.get(eventName).forEach(callback => callback(data));
        }
    }

    generateMockServices() {
        return [
            { service: 'jellyfin', name: 'Jellyfin', description: 'Media Server', icon: '🎬', running: true, healthStatus: 'healthy', port: 8096, responseTime: 120, version: '10.8.10' },
            { service: 'sonarr', name: 'Sonarr', description: 'TV Show Manager', icon: '📺', running: true, healthStatus: 'healthy', port: 8989, responseTime: 80, version: '3.0.10' },
            { service: 'radarr', name: 'Radarr', description: 'Movie Manager', icon: '🎥', running: true, healthStatus: 'warning', port: 7878, responseTime: 1500, version: '4.2.4' },
            { service: 'qbittorrent', name: 'qBittorrent', description: 'Torrent Client', icon: '⬇️', running: true, healthStatus: 'unhealthy', port: 8080, responseTime: 5000, version: '4.5.0' },
            { service: 'prowlarr', name: 'Prowlarr', description: 'Indexer Manager', icon: '🔍', running: false, healthStatus: 'stopped', port: 9696, responseTime: 0, version: '1.0.0' },
            { service: 'overseerr', name: 'Overseerr', description: 'Request Manager', icon: '🎯', running: true, healthStatus: 'healthy', port: 5055, responseTime: 250, version: '1.33.2' },
        ];
    }

    async getAllServices() {
        console.log('MockDockerClient: getAllServices called');
        this.emit('services-updated', this.mockServices);
        return this.mockServices;
    }

    async startServices(serviceNames = []) {
        console.log(`MockDockerClient: startServices called for`, serviceNames);
        if (serviceNames.length === 0) { // Start all
            this.mockServices.forEach(s => s.running = true);
        } else {
            serviceNames.forEach(name => {
                const service = this.mockServices.find(s => s.service === name);
                if (service) service.running = true;
            });
        }
        this.emit('services-updated', this.mockServices);
        this.emit('services-started', { success: true, services: serviceNames });
        return { success: true };
    }

    async stopServices(serviceNames = []) {
        console.log(`MockDockerClient: stopServices called for`, serviceNames);
        if (serviceNames.length === 0) { // Stop all
            this.mockServices.forEach(s => s.running = false);
        } else {
            serviceNames.forEach(name => {
                const service = this.mockServices.find(s => s.service === name);
                if (service) service.running = false;
            });
        }
        this.emit('services-updated', this.mockServices);
        this.emit('services-stopped', { success: true, services: serviceNames });
        return { success: true };
    }

    async restartServices(serviceNames = []) {
        console.log(`MockDockerClient: restartServices called for`, serviceNames);
        // Simulate a restart delay
        this.stopServices(serviceNames);
        setTimeout(() => {
            this.startServices(serviceNames);
        }, 2000);
        return { success: true };
    }

    async generateHealthReport() {
        console.log('MockDockerClient: generateHealthReport called');
        return {
            timestamp: new Date().toISOString(),
            overallStatus: 'healthy',
            services: this.mockServices
        };
    }
}
