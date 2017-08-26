# Verify packages
libs.required = c("readr", "data.table", "purrr", "stringr", "ggplot2")
libs.installed = installed.packages()[, 'Package']
libs.not.installed = sapply(libs.required, function (x) !(x %in% libs.installed))

# Install dependencies
if (sum(libs.not.installed) >= 1) {
  install.packages(libs.required[as.vector(libs.not.installed)], repos='http://cran.us.r-project.org')
}

# Load libraries
sapply(libs.required, library , character.only = TRUE)

" Data specification
   + http://dados.gov.br/dataset/spm_odm_2009
   + http://dados.gov.br/dataset/spm_odm_2010
   + http://dados.gov.br/dataset/spm_odm_2011
"

# Define URLs to download files
urls = c(
			"http://geoservicos.inde.gov.br/geoserver/SPM/wms?service=WFS&version=1.0.0&request=GetFeature&typeName=SPM:ODM_2009&outputFormat=CSV",
			"http://geoservicos.inde.gov.br/geoserver/SPM/wms?service=WFS&version=1.0.0&request=GetFeature&typeName=SPM:ODM_2010&outputFormat=CSV",
			"http://geoservicos.inde.gov.br/geoserver/SPM/wms?service=WFS&version=1.0.0&request=GetFeature&typeName=SPM:ODM_2011&outputFormat=CSV"
		)

# Define filenames
files.names = map_chr(urls, str_extract, "ODM_\\d{4}") %>% paste0(".csv")

# Not yet downloaded files
files.not.downloades.indexes = !map_lgl(files.names, file.exists)

# Download files
map2(urls[files.not.downloades.indexes],  files.names[files.not.downloades.indexes], download.file)
set_progress(0.25)

# Define dataframe to save performance data

libraries = c("utils:read.csv", "readr:read_csv", "data.table:fread")
time.loading = integer(3)
names(time.loading) = libraries

# Test read.csv [default library]
time.init = Sys.time()

df = read.csv(files.names[1])
df = read.csv(files.names[2])
df = read.csv(files.names[3])

time.loading[1] = as.double(Sys.time() - time.init)

set_progress(0.5)

# Test read_csv [readr]
time.init = Sys.time()

df = read_csv(files.names[1])
df = read_csv(files.names[2])
df = read_csv(files.names[3])

time.loading[2] = as.double(Sys.time() - time.init)

set_progress(0.75)

# Test fread [data.table]
time.init = Sys.time()

df = fread(files.names[1])
df = fread(files.names[2])
df = fread(files.names[3])

time.loading[3] = as.double(Sys.time() - time.init)

set_progress(0.99)

# Plot results
jpeg(file.path(params$output_dir, "Plot.jpg"))

barplot(time.loading,
        main = "Performance analysis of Data Frame loading",
        ylab = "Loading time (s)",
        xlab = "Libraries",
        col = c("#e0e0e0", "#e0e0e0","#66BB6A"))

dev.off()

set_progress(1.0)