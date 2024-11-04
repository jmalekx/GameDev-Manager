<template>
    <div class="modal fade" id="GameModal" tabindex="-1" aria-labelledby="GameModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="GameModalLabel">{{ isEditing ? 'Edit Game' : 'Add New Game' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label for="title" class="form-label">Title</label>
                            <input type="text" id="title" v-model="game.title" class="form-control" required />
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea id="description" v-model="game.description" class="form-control" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="release_date" class="form-label">Release Date</label>
                            <input type="date" id="release_date" v-model="game.release_date" class="form-control" required />
                        </div>
                        <div class="mb-3">
                            <label for="platform" class="form-label">Platform</label>
                            <select id="platform" v-model="game.platform" class="form-select" required>
                                <option value="PC">Computer/Laptop</option>
                                <option value="Console">Console</option>
                                <option value="Mobile">Android/iOS</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="developer" class="form-label">Select Developer</label>
                            <select v-model="selectedDeveloperId" class="form-select" required>
                                <option disabled value="">Please select one</option>
                                <option v-for="developer in developers" :key="developer.id" :value="developer.id">
                                    {{ developer.name }}
                                </option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="role" class="form-label">Select Role</label>
                            <select v-model="selectedRole" class="form-select" required>
                                <option disabled value="">Please select a role</option>
                                <option v-for="role in roles" :key="role" :value="role">
                                    {{ role }}
                                </option>
                            </select>
                        </div>

                        <button type="button" class="btn btn-secondary" @click="addDeveloperRole">Add Developer Role</button>

                        <ul class="mt-3">
                            <li v-for="(devRole, index) in developerRoles" :key="index">
                                <span>Developer: {{ devRole.developerName }}, Role: 
                                    <select v-model="devRole.role" class="form-select d-inline-block" style="width: auto;" @change="updateDeveloperRole(index)" required>
                                        <option v-for="role in roles" :key="role" :value="role">
                                            {{ role }}
                                        </option>
                                    </select>
                                </span>
                                <button type="button" class="btn btn-danger btn-sm" @click="removeDeveloperRole(index)">Remove</button>
                            </li>
                        </ul>

                        <button type="submit" class="btn btn-primary">
                            {{ isEditing ? 'Save Changes' : 'Add Game' }}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { baseUrl } from '../main.js';

export default {
    data() {
        return {
            game: {
                title: '',
                description: '',
                release_date: '',
                platform: 'PC', // Default platform
            },
            developers: [], // List of developers
            roles: [
                'Level Designer',
                'Programmer',
                'Artist',
                'Animator',
                'Sound Designer',
                'Project Manager',
                'UI/UX Designer'
            ],
            selectedDeveloperId: null, // Selected developer ID
            selectedRole: null, // Selected role
            developerRoles: [], // Array to hold developer-role pairs
            isEditing: false, // Flag to indicate editing mode
        };
    },
    props: {
        gameToEdit: {
            type: Object,
            default: null,
        },
    },
    watch: {
        gameToEdit: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.isEditing = true;
                    this.game = { ...newVal }; // Create a shallow copy
                    this.developerRoles = newVal.developers.map(dev => ({
                        developerId: dev.developer_id,
                        developerName: dev.developer_name,
                        role: dev.role,
                    }));
                } else {
                    this.isEditing = false;
                    this.resetForm();
                }
            },
        },
    },
    methods: {
        async fetchDevelopers() {
            const response = await fetch(`${baseUrl}/api/developers/`);
            const data = await response.json();
            this.developers = data.developers;
        },
        resetForm() {
            this.game = {
                title: '',
                description: '',
                release_date: '',
                platform: 'PC',
            };
            this.developerRoles = [];
            this.selectedDeveloperId = null;
            this.selectedRole = null;
        },
        addDeveloperRole() {
            if (this.selectedDeveloperId && this.selectedRole) {
                const developer = this.developers.find(dev => dev.id === this.selectedDeveloperId);
                if (developer) {
                    // Push developer role with both ID and role
                    this.developerRoles.push({ 
                        developerId: developer.id, 
                        developerName: developer.name, 
                        role: this.selectedRole 
                    });
                    // Clear selected values after adding
                    this.selectedDeveloperId = null; 
                    this.selectedRole = null; 
                }
            } else {
                alert('Please select a developer and a role before adding.');
            }
        },
        removeDeveloperRole(index) {
            this.developerRoles.splice(index, 1);
        },
        async submitForm() {
            if (this.developerRoles.length === 0) {
                alert('At least one developer must be added.');
                return; // Prevent submission if there are no developers
            }

            const payload = {
                ...this.game,
                developers: this.developerRoles.map(devRole => ({
                    id: devRole.developerId, // Change to 'id' if that’s how the backend expects it
                    role: devRole.role,
                })),
            };

            try {
                if (this.isEditing) {
                    await this.editGame(payload);
                } else {
                    await this.addGame(payload);
                }
                this.$emit('fetch-games');
                this.resetForm();
                this.closeModal();
            } catch (error) {
                console.error('Error submitting form:', error);
                alert('An error occurred while saving the game. Please try again.');
            }
        },
        async editGame(payload) {
            const response = await fetch(`${baseUrl}/api/games/${this.game.id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                console.error('Error editing game:', await response.text());
                throw new Error('Failed to edit game');
            } else {
                const data = await response.json();
                console.log('Game updated:', data); // Log the response for debugging
            }
        },
        async addGame(payload) {
            const response = await fetch(`${baseUrl}/api/games/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                console.error('Error adding game:', await response.text());
                throw new Error('Failed to add game');
            } else {
                const data = await response.json();
                console.log('Game added:', data); // Log the response for debugging
            }
        },
        closeModal() {
            const modal = bootstrap.Modal.getInstance(document.getElementById('GameModal'));
            modal.hide();
        },
    },
    mounted() {
        this.fetchDevelopers(); // Fetch developers when the component is mounted
    },
};
</script>

<style scoped>
.modal-body {
    padding: 20px;
}
</style>
