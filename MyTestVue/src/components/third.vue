<template>
  <div id="third">
    <select class="selectedProject" v-model="selectedproject">
      <option v-for="project in projects">{{ project.name }}</option>
    </select>
    <!-- <span>{{selectedproject}}</span> -->
    <select class="selectedBrance" v-model="selectedbranch">
      <option v-for="branch in branches">{{ branch.name }}</option>
    </select>
    <!-- <p>{{selectedbranch}}</p> -->
    <select class="selectedTag" v-model="selectedtag">
      <option v-for="tag in tags">{{ tag.name }}</option>
    </select>
    <br></br>
    <button v-on:click="pushTest">提交测试</button>
    <button v-on:click="pushProd">提交生产</button>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        projects: [],
        branches: [],
        tags: [],
        selectedproject: '',
        selectedbranch: '',
        selectedtag: '',
      }
    },
    created() {
      this.getProject();
    },
    // computed: {
    //   get_tags: function () {
    //     for (var i=0;i<this.projects.length;i++) {
    //       if (this.projects[i].name === this.selectedproject) {
    //         var branches = this.getTags(this.projects[i].id);
    //         this.branches = branches
    //         return branches
    //       }
    //     }
    //   },
    //   get_branches: function(){
    //     for (var i=0;i<this.projects.length;i++) {
    //       if (this.projects[i].name === this.selectedproject) {
    //         var branches = this.getBranches(this.projects[i].id);
    //         this.branches = branches
    //         return branches
    //       }
    //     }
    //   }
    // },
    watch: {
      'selectedproject': function (val) {
        for (var i=0;i<this.projects.length;i++) {
          if (this.projects[i].name === val) {
            this.getTags(this.projects[i].id);
            this.getBranches(this.projects[i].id);
          }
        }
      },
    },
    methods: {
      getProject: function() {
        this.axios.get('http://127.0.0.1:8000/api/getproject/').then((response) => {
          this.projects = response.data;
        }).then(function(response) {
          console.log(response)
        });
      },
      getTags: function(id) {
        this.axios.post('http://127.0.0.1:8000/api/gettags/', {
          project_id: id},
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'}
        })
        .then((response) => {
          this.tags = response.data;
          // console.log(response);
          // return tags
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      getBranches: function(id) {
        this.axios.post('http://127.0.0.1:8000/api/getbranches/', {
          project_id: id},
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'}
        })
        .then((response) => {
           this.branches = response.data;
          // console.log(response);
          // return branches
        })
        .catch(function (error) {
          console.log(error);
        });
      },
      pushTest: function() {
        let project = this.selectedproject;
        let branch = this.selectedbranch;
        let tag = this.selectedtag;
        this.axios.post('http://127.0.0.1:8000/api/pushTest/', {
          project: project,
          branch: branch,
          tag: tag,
          },
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'}
        })
        .then((response) => {
           return response.data
        })
        .catch(function (error) {
          console.log(error);
        });
      },
    }
  }
</script>
