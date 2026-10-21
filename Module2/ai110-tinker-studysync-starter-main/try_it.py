from ranking import load_study_spots, rank_study_spots, format_results

profile = {
    "max_noise": input("Max noise (quiet/moderate/loud): ").strip().lower(),
    "max_distance": float(input("Max distance in miles: ")),
    "min_seats": int(input("Min seats: ")),
}
k = int(input("How many results: "))

format_results(rank_study_spots(profile, load_study_spots("data/study_spots.csv"), k=k))
