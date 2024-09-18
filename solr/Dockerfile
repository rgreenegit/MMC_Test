FROM solr:8.11.1

# Copy your cores into the image
COPY ./cores /var/solr/data

# Expose the Solr admin port
EXPOSE 8983

# Define a default command to run when the container starts
CMD ["solr-precreate", "core1"]