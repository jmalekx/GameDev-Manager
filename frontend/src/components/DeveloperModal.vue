<template>
    <div class="modal fade" id="DeveloperModal" tabindex="-1" aria-labelledby="DeveloperModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="DeveloperModalLabel">{{ isEditing ? 'Edit Developer' : 'Add New Developer' }}</h5>
                    <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitForm">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name</label>
                            <input type="text" v-model="developer.name" class="form-control" id="name" required />
                        </div>
                        <div class="mb-3">
                            <label for="about" class="form-label">About</label>
                            <textarea v-model="developer.about" class="form-control" id="about"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="experience_years" class="form-label">Experience (Years)</label>
                            <input type="number" v-model="developer.experience_years" class="form-control" id="experience_years" required />
                        </div>
                        <div class="mb-3">
                            <label for="available_to_hire" class="form-label">Available to Hire</label>
                            <select v-model="developer.available_to_hire" class="form-select" id="available_to_hire" required>
                                <option :value="true">Yes</option>
                                <option :value="false">No</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label for="join_date" class="form-label">Join Date</label>
                            <input type="date" v-model="developer.join_date" class="form-control" id="join_date" required />
                        </div>
                        <button type="submit" class="btn btn-primary">{{ isEditing ? 'Update Developer' : 'Add Developer' }}</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="toast" id="successToast" role="alert" aria-live="assertive" aria-atomic="true" style="position: absolute; top: 20px; right: 20px; z-index: 1050;">
            <div class="toast-header">
                <strong class="me-auto">Success</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                Developer added/updated successfully!
            </div>
        </div>
    </div>
</template>

<script>
import { baseUrl } from '../main.js';

export default {
    data() {
        return {
            developer: {
                name: '',
                about: '',
                experience_years: '',
                available_to_hire: true,
                join_date: ''
            },
            isEditing: false,
        };
    },
    props: {
        developerToEdit: {
            type: Object,
            default: null,
        }
    },
    watch: {
        developerToEdit: {
            immediate: true,
            handler(newVal) {
                if (newVal) {
                    this.isEditing = true;
                    this.developer = { ...newVal }; // Deep clone to avoid mutation
                } else {
                    this.isEditing = false;
                    this.resetForm(); // Reset the form for new developer
                }
            }
        }
    },
    methods: {
        resetForm() {
            this.developer = {
                name: '',
                about: '',
                experience_years: '',
                available_to_hire: true,
                join_date: ''
            };
        },
        closeModal() {
            this.resetForm();
        },
        async submitForm() {
            const url = this.isEditing 
                ? `${baseUrl}/api/developers/${this.developer.id}/` 
                : `${baseUrl}/api/developers/`;
            const method = this.isEditing ? 'PUT' : 'POST';

            try {
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.developer),
                });

                if (response.ok) {
                    await response.json(); // Optionally use the response if needed
                    this.$emit('fetch-developers'); // Refresh the developer list
                    this.resetForm(); // Reset the form fields

                    // Show success toast
                    const toastEl = document.getElementById('successToast');
                    const toast = new bootstrap.Toast(toastEl);
                    toast.show();
                } else {
                    const errorText = await response.text(); // Get the response text to log
                    console.error('Error updating developer:', errorText);
                    alert(`Error updating developer: ${response.status} - ${response.statusText}. Please check server logs for more details.`);
                }
            } catch (error) {
                console.error('Fetch error:', error);
                alert('An error occurred while trying to update the developer.');
            }
        }
    }
};
</script>

<style scoped>
.modal-body {
    padding: 20px;
}
</style>
