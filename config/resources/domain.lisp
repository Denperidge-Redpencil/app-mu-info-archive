(in-package :mu-cl-resources)

(define-resource repo ()
  :class (s-prefix "ext:Repo")
  :properties `((:title :string ,(s-prefix "dct:title"))
                (:description :string ,(s-prefix "dct:description"))
                (:category :url ,(s-prefix "ext:category"))
                (:repo-url :url ,(s-prefix "ext:repositoryUrl"))
                (:image-url :url ,(s-prefix "ext:imageUrl"))
                (:homepage-url :url ,(s-prefix "ext:homepageUrl"))
                )
  :has-many `((revision :via ,(s-prefix "ext:hasRevision")
                        :as "revisions")
              (command :via ,(s-prefix "ext:hasCommand")
                       :as "commands"))
  :features '(no-pagination-defaults)
  :resource-base (s-url "http://info.mu.semte.ch/repos/")
  :on-path "repos")

(define-resource revision ()
  :class (s-prefix "ext:RepoRevision")
  :properties `((:image-tag :string ,(s-prefix "ext:revisionImageTag"))
                (:image-url :string ,(s-prefix "ext:revisionImageUrl"))
                (:repo-tag :string ,(s-prefix "ext:revisionRepoTag"))
                (:repo-url :string ,(s-prefix "ext:revisionRepoUrl"))
                (:readme :string ,(s-prefix "ext:readme"))
                )
  :has-one `((repo :via ,(s-prefix "ext:hasRevision")
                           :inverse t
                           :as "repo"))
  :features '(no-pagination-defaults)
  :resource-base (s-url "http://info.mu.semte.ch/microservice-revisions/")
  :on-path "repo-revisions")

(define-resource command ()
  :class (s-prefix "ext:MicroserviceCommand")
  :properties `((:title :string ,(s-prefix "ext:commandTitle"))
                (:shell-command :string ,(s-prefix "ext:shellCommand"))
                (:description :string ,(s-prefix "dct:description")))
  :has-one `((microservice :via ,(s-prefix "ext:hasCommand")
                           :inverse t
                           :as "microservice"))
  :features '(no-pagination-defaults)
  :resource-base (s-url "http://info.mu.semte.ch/microservice-commands/")
  :on-path "microservice-commands")
