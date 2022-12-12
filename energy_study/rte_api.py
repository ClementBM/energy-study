# https://data.rte-france.com/catalog/consumption

# Il est conseillé de faire un appel par heure à ce service
# et de ne pas dépasser une période de 155 jours par appel.


# swagger code generation
# https://swagger.io/tools/swagger-codegen/
# Online generator for api client

curl -X POST -H "content-type:application/json" -d '{"swaggerUrl":"https://petstore.swagger.io/v2/swagger.json"}' https://generator.swagger.io/api/gen/clients/ruby

