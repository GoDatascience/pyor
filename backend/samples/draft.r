# Verifica pacotes não instalados
libs.required = c("readr", "data.table", "purrr", "stringr", "ggplot2")
libs.installed = installed.packages()[, 'Package']
libs.not.installed = sapply(libs.required, function (x) !(x %in% libs.installed))

# Instala Dependencias
if (sum(libs.not.installed) >= 1) {
  install.packages(libs.required[as.vector(libs.not.installed)], repos='http://cran.us.r-project.org')
}

# Carrga Bibliotecas
sapply(libs.required, library , character.only = TRUE)

" Especificações dos dados
   + http://dados.gov.br/dataset/spm_odm_2009
   + http://dados.gov.br/dataset/spm_odm_2010
   + http://dados.gov.br/dataset/spm_odm_2011
"

# Define URLS para buscar arquivos
urls = c(
			"http://geoservicos.inde.gov.br/geoserver/SPM/wms?service=WFS&version=1.0.0&request=GetFeature&typeName=SPM:ODM_2009&outputFormat=CSV",
			"http://geoservicos.inde.gov.br/geoserver/SPM/wms?service=WFS&version=1.0.0&request=GetFeature&typeName=SPM:ODM_2010&outputFormat=CSV",
			"http://geoservicos.inde.gov.br/geoserver/SPM/wms?service=WFS&version=1.0.0&request=GetFeature&typeName=SPM:ODM_2011&outputFormat=CSV"
		)

# Define nomes dos arquivos
files.names = map_chr(urls, str_extract, "ODM_\\d{4}") %>% paste0(".csv")

# Arquivos não baixados
files.not.downloades.indexes = !map_lgl(files.names, file.exists)

# Baixa os arquivos
map2(urls[files.not.downloades.indexes],  files.names[files.not.downloades.indexes], download.file)
set_progress(0.25)

# Define data frame para guardar desempenhos

bibliotecas = c("utils:read.csv", "readr:read_csv", "data.table:fread")
tempo.carga = integer(3)
names(tempo.carga) = bibliotecas

# Teste read.csv [Biblioteca Padrão]
time.init = Sys.time()

df = read.csv(files.names[1])
df = read.csv(files.names[2])
df = read.csv(files.names[3])

tempo.carga[1] = as.double(Sys.time() - time.init)

set_progress(0.5)

# Teste read_csv [Biblioteca readr]
time.init = Sys.time()

df = read_csv(files.names[1])
df = read_csv(files.names[2])
df = read_csv(files.names[3])

tempo.carga[2] = as.double(Sys.time() - time.init)

set_progress(0.75)

# Teste fread [Biblioteca data.table]
time.init = Sys.time()

df = fread(files.names[1])
df = fread(files.names[2])
df = fread(files.names[3])

tempo.carga[3] = as.double(Sys.time() - time.init)

set_progress(0.99)

# Plota resultados
jpeg(file.path(params$output_dir, "Grafico.jpg"))

barplot(tempo.carga,
        main = "Análise de desempenho de carga de Data Frames",
        ylab = "Tempo de carga (s)",
        xlab = "Bibliotecas",
        col = c("#e0e0e0", "#e0e0e0","#66BB6A"))

dev.off()

set_progress(1.0)