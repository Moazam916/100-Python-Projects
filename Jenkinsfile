pipeline {
    agent any
    parameters {
        string(name: 'ENVIRONMENT', defaultValue: 'dev', description: 'Specify the environment (dev, acpt, prod)')
    }
    stages {
      stage("testing stage"){
        steps{
          script{
            echo "this is just demo"
          } // end of script
        } // end of steps
      } // end of stage
    } // end of stages
} // end of pipeline
