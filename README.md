# mu-project

Bootstrap a mu.semte.ch microservices environment in three easy steps.

## How to

Setting up your environment is done in three easy steps:  first you configure the running microservices and their names in `docker-compose.yml`, then you configure how requests are dispatched in `config/dispatcher.ex`, and lastly you start everything.

### Hooking things up with docker-compose

Alter the `docker-compose.yml` file so it contains all microservices you need.  The example content should be clear, but you can find more information in the [Docker Compose documentation](https://docs.docker.com/compose/).  Don't remove the `identifier` and `db` container, they are respectively the entry-point and the database of your application.  Don't forget to link the necessary microservices to the dispatcher and the database to the microservices.

### Configure the dispatcher

Next, alter the file `config/dispatcher.ex` based on the example that is there by default.  Dispatch requests to the necessary microservices based on the names you used for the microservice.

### Boot up the system

Boot your microservices-enabled system using docker-compose.

    cd /path/to/mu-project
    docker-compose up

You can shut down using `docker-compose stop` and remove everything using `docker-compose rm`.

## Reference
Please also check the docstrings and typing included in the code!

### Repo model
This is defined in [config/resources/domain.lisp](config/resources/domain.lisp) and [the Repo class](app/Repo.py). Here's a human-readable overview!
| Attribute          | Type             | Description |
| ------------------ | ---------------- | ----------- |
| category           | `URI`            | What type of repository it is. 
| name               | `String`         | Repository and - by extension - microservice name. |
| homepage-url       | `String/URL`     | Homepage url |
||||
| repo-url            | `String/URL`    | Repository url |
| repo-branch         | `String`        | Branch to be used in production? |
| repo-tag            | `String`        | Release tag from the repository |
||||
| image-url           | `String/URL`    | Container image url |
| image-tag           | `String`       | Release tag for the container |



| available_versions | `Array[Revision]`| Available versions for the microservice. Should include the Docker tags |
| installed_version  | `Revision`       | The version that is installed! |
| readme?            | `String`         | Content of the README |
| documentation?     | `String`?        | splitted up readme thing for each version (divio-docs-gen) |


### overrides.conf
You can configure [overrides.conf](overrides.conf) in case you break your own Category naming convention, or want to archive specific repositories without changing the git repository.
The syntax is as follows:
```conf
[regex-.*-for-repo-name]
Category=tools  # Optional, reassigns to the category with specified 
ImageName=mu-login-service  # Optional, overrides the container image name for this repo
```

## License
This project is licensed under [the MIT License](LICENSE).
