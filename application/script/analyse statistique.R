
#================================================================
#=============Partie nettoyage et importation====================
#================================================================

#importation des modules 
library(tidyr)
library(readr)
library(ggplot2)
library(dplyr)

#importation des fichiers et ajout de la colonne année

df2019 <- read.csv("C:/Users/yessi/OneDrive/Desktop/cours/semestre2/sae/sae python/sae_py/application/data/Données Cartographie 2019.csv", sep=";",fileEncoding = "UTF-8")
df2019$année <- "2019"
df2020 <- read.csv("C:/Users/yessi/OneDrive/Desktop/cours/semestre2/sae/sae python/sae_py/application/data/Données Cartographie 2020.csv", sep=";")
df2020$année <- "2020"
df2021 <- read.csv("C:/Users/yessi/OneDrive/Desktop/cours/semestre2/sae/sae python/sae_py/application/data/Données Cartographie 2021.csv", sep=";")
df2021$année <- "2021"

#fusion des 3 année
df_all <- bind_rows(df2019, df2020, df2021)

#nettoyage des colonne 
colonnes_num <- c("entrées", "séances", "PdM.en.entrées.des.films.français","PdM.en.entrées.des.films.américains","PdM.en.entrées.des.films.européens")
for (col in colonnes_num) {
  df_all[[col]] <- as.numeric(gsub(",", ".", df_all[[col]]))
}



#================================================================
#=============Partie création des graphique======================
#================================================================

# Entrées totales par année

df_all %>%
  group_by(année) %>%
  summarise(entrees_totales = sum(entrées, na.rm = TRUE)) %>%
  ggplot(aes(x = factor(année), y = entrees_totales)) +
  geom_col(fill = "steelblue") +
  labs(title = "Entrées totales par année", x = "année", y = "Entrées")

# Nombre moyen de séances par année

df_all %>%
  group_by(année) %>%
  summarise(moy_séances = mean(séances, na.rm = TRUE)) %>%
  ggplot(aes(x = factor(année), y = moy_séances)) +
  geom_col(fill = "darkgreen") +
  labs(title = "Nombre moyen de séances par année", x = "Année", y = "Séances moyennes")

# Part moyenne des films français et americain 
df_pdm <- df_all %>%
  group_by(année) %>%
  summarise(
    français = mean(`PdM.en.entrées.des.films.français`, na.rm = TRUE),
    américains = mean(`PdM.en.entrées.des.films.américains`, na.rm = TRUE),
    européens = mean(`PdM.en.entrées.des.films.européens`, na.rm = TRUE)
    
  ) %>%
  pivot_longer(cols = c("français", "américains","européens"), names_to = "nationalité", values_to = "part")

# Graphique combiné

ggplot(df_pdm, aes(x = année, y = part, color = nationalité, group = nationalité)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 2) +
  labs(title = "Part moyenne des films français, américains et européen",
       x = "Année", y = "Part de marché (%)") +
  theme_minimal()
# Détermination du top 5 des régions avec le plus d'entrées

top_regions <- df_all %>%
  group_by(région.administrative) %>%
  summarise(total_entrees = sum(entrées, na.rm = TRUE)) %>%
  slice_max(order_by = total_entrees, n = 5) %>%
  pull(région.administrative)


# Évolution des entrées dans les 5 régions principales

df_all %>%
  filter(région.administrative %in% top_regions) %>%
  group_by(année, région.administrative) %>%
  summarise(total_entrees = sum(entrées, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(x = année, y = total_entrees, color = région.administrative, group = région.administrative)) +
  geom_line(linewidth = 1.2) +
  geom_point() +
  labs(title = "Évolution des entrées par région",
       x = "Année", y = "Entrées")

# Top 5 des régions avec le plus de cinémas (distincts)

top_regions <- df_all %>%
  filter(!is.na(région.administrative)) %>%
  group_by(région.administrative) %>%
  summarise(total_cinemas = n_distinct(nom, na.rm = TRUE)) %>%
  slice_max(order_by = total_cinemas, n = 5) %>%
  pull(région.administrative)

# Évolution du nombre de cinémas dans les top 5 régions

df_all %>%
  filter(région.administrative %in% top_regions, !is.na(année)) %>%
  group_by(année, région.administrative) %>%
  summarise(nb_cinemas = n_distinct(nom, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(x = année, y = nb_cinemas, color = région.administrative, group = région.administrative)) +
  geom_line(linewidth = 1.2) +
  geom_point(size = 2) +
  labs(title = "Évolution du nombre de cinémas par année et region",
       x = "Année", y = "Nombre de cinémas") +
  theme_minimal()

# Top 5 cinémas avec le plus d’écrans

top5_ecrans <- df_all %>%
  filter(!is.na(région.administrative), !is.na(écrans)) %>%
  group_by(région.administrative) %>%
  summarise(max_ecrans = max(écrans, na.rm = TRUE)) %>%
  arrange(desc(max_ecrans)) %>%
  slice_head(n = 5) %>%
  pull(région.administrative)

# Évolution du nombre d’écrans

df_all %>%
  filter(région.administrative %in% top5_ecrans, !is.na(année), !is.na(écrans)) %>%
  group_by(année, région.administrative) %>%
  summarise(nb_ecrans = max(écrans, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(x = année, y = nb_ecrans, color = région.administrative, group = région.administrative)) +
  geom_line(linewidth = 1.2) +
  geom_point() +
  labs(title = "Évolution du nombre d’écrans",
       x = "Année", y = "Nombre d’écrans") +
  theme_minimal()

# Top 5 cinémas avec le plus de fauteuils

top5_fauteuils <- df_all %>%
  filter(!is.na(région.administrative), !is.na(fauteuils)) %>%
  group_by(région.administrative) %>%
  summarise(max_fauteuils = max(fauteuils, na.rm = TRUE)) %>%
  arrange(desc(max_fauteuils)) %>%
  slice_head(n = 5) %>%
  pull(région.administrative)
# Évolution du nombre de fauteuils

df_all %>%
  filter(région.administrative %in% top5_fauteuils, !is.na(année), !is.na(fauteuils)) %>%
  group_by(année, région.administrative) %>%
  summarise(nb_fauteuils = max(fauteuils, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(x = année, y = nb_fauteuils, color = région.administrative, group = région.administrative)) +
  geom_line(linewidth = 1.2) +
  geom_point() +
  labs(title = "Évolution du nombre de fauteuils ",
       x = "Année", y = "Nombre de fauteuils") +
  theme_minimal()

# Top 5 cinémas avec le plus de séances

top5_seances <- df_all %>%
  filter(!is.na(région.administrative), !is.na(séances)) %>%
  group_by(région.administrative) %>%
  summarise(total_seances = sum(séances, na.rm = TRUE)) %>%
  arrange(desc(total_seances)) %>%
  slice_head(n = 5) %>%
  pull(région.administrative)

# Évolution du nombre de séances

df_all %>%
  filter(région.administrative %in% top5_seances, !is.na(année), !is.na(séances)) %>%
  group_by(année, région.administrative) %>%
  summarise(nb_seances = sum(séances, na.rm = TRUE), .groups = "drop") %>%
  ggplot(aes(x = année, y = nb_seances, color = région.administrative, group = région.administrative)) +
  geom_line(linewidth = 1.2) +
  geom_point() +
  labs(title = "Évolution du nombre de séances",
       x = "Année", y = "Nombre de séances") +
  theme_minimal()
