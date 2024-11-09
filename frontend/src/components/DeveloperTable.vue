<template>
    <div>
        <div class="d-flex justify-content-between mb-3">
            <h3 class="text fw-bold">Developers</h3>
            <button type="button" class="btn btn-success btn-lg" @click="openAddModal">
                <i class="bi bi-plus-circle me-2"></i>Add New Developer
            </button>
        </div>
        <table class="table">
            <thead>
                <tr class="align-middle fs-5 py-3">
                    <th scope="col">#</th>
                    <th scope="col">Name</th>
                    <th scope="col">About</th>
                    <th scope="col">Experience</th>
                    <th scope="col">Availability</th>
                    <th scope="col">Join Date</th>
                    <th scope="col">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(developer, index) in developers" :key="developer.id" class="align-middle">
                    <th scope="row">{{ index + 1 }}</th>
                    <td>{{ developer.name }}</td>
                    <td>{{ developer.about }}</td>
                    <td>
                        <span class="badge bg-secondary">
                            {{ developer.experience_years }} years
                        </span>
                    </td>
                    <td>
                        <span class="badge" 
                            :class="developer.available_to_hire ? 'bg-success text-dark' : 'bg-danger text-dark'">
                            {{ developer.available_to_hire ? 'Yes' : 'No' }}
                        </span>
                    </td>
                    <td>{{ developer.join_date }}</td>
                    <td>
                        <button 
                            class="btn btn-sm btn-warning me-2"
                            @click="openEditModal(developer)"
                        >
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button 
                            class="btn btn-sm btn-danger" 
                            @click="deleteDeveloper(developer)"
                        >
                            <i class="bi bi-trash"></i>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <DeveloperModal 
            :developerToEdit="developerToEdit"
            @fetch-developers="$emit('fetch-developers')"
        />
    </div>
</template>

<script>
import DeveloperModal from './DeveloperModal.vue';
import { baseUrl } from '../main.js';

export default {
    components: {
        DeveloperModal,
    },
    props: {
        developers: {
            type: Array,
            required: true,
        },
    },
    data() {
        return {
            developerToEdit: null,
        };
    },
    methods: {
        openEditModal(developer) {
            this.developerToEdit = developer;
            this.$nextTick(() => {
                const modal = new bootstrap.Modal(document.getElementById('DeveloperModal'));
                modal.show();
            });
        },
        openAddModal() {
            this.developerToEdit = null;
            this.$nextTick(() => {
                const modal = new bootstrap.Modal(document.getElementById('DeveloperModal'));
                modal.show();
            });
        },
        async deleteDeveloper(developer) {
            if (confirm(`Are you sure you want to delete developer '${developer.name}'?`)) {
                try {
                    const response = await fetch(`${baseUrl}/api/developers/${developer.id}/`, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    });

                    if (response.ok) {
                        this.$emit('fetch-developers'); //refresh developer list
                    } else {
                        const errorData = await response.json();
                        alert(`Error deleting developer: ${errorData.error}`);
                    }
                } catch (error) {
                    console.error('Error deleting developer:', error);
                    alert('An error occurred while trying to delete the developer.');
                }
            }
        },
    },
};
</script>
