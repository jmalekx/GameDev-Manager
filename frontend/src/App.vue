<template>
    <div class="container pt-4">
        <div class="text-center mb-4">
            <h1 class="display-4">
                API Client
            </h1>
        </div>

        <!-- Tabs -->
        <ul class="nav nav-tabs mb-4" id="modelTabs" role="tablist">
            <li class="nav-item">
                <button class="nav-link active" id="developers-tab" data-bs-toggle="tab" data-bs-target="#developers"
                    type="button" role="tab" aria-controls="developers" aria-selected="true" @click="setActiveTab('developers')">
                    Developers
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="games-tab" data-bs-toggle="tab" data-bs-target="#games" type="button"
                    role="tab" aria-controls="games" aria-selected="false" @click="setActiveTab('games')">
                    Games
                </button>
            </li>
        </ul>

       
        <div class="tab-content" id="modelTabContent">
            <!-- Developer Tab -->
            <div class="tab-pane fade show active" id="developers" role="tabpanel" aria-labelledby="developers-tab">
                <DeveloperTable 
                    v-if="activeTab === 'developers'" 
                    :developers="developers" 
                    @fetch-developers="fetchDevelopers" 
                />
            </div>

            <!-- Game Tab -->
            <div class="tab-pane fade" id="games" role="tabpanel" aria-labelledby="games-tab">
                <GameTable
                    v-if="activeTab === 'games'" 
                    :games="games" 
                    @fetch-games="fetchGames" 
                />
            </div>
        </div>

    </div>
</template>

<script>
    import DeveloperTable from './components/DeveloperTable.vue'
    import GameTable from './components/GameTable.vue'
    import { baseUrl } from './main.js';

    export default {
        components:{
            DeveloperTable,
            GameTable,
        },
        data() {
            return {
                activeTab: 'developers',
                developers: [],
                games: [],
                developerToEdit: null,
                gameToEdit: null,
            };
        },
        methods: {
            setActiveTab(tab) { //check which tab is active to fetch data (e.g if add new dev, make sure it is updated when you go to games)
                this.activeTab = tab;
                if (tab === 'games') {
                    this.fetchGames();
                } else if (tab === 'developers') {
                    this.fetchDevelopers();
                }
            },
            async fetchDevelopers() {
                const response = await fetch(`${baseUrl}/api/developers/`);
                const data = await response.json();
                this.developers = data.developers;
            },
            async fetchGames() {
                const response = await fetch(`${baseUrl}/api/games/`);
                const data = await response.json();
                this.games = data.games;
            },
        },
        mounted() {
            this.fetchDevelopers(); // Fetch developers on initial load
        }
    };
</script>