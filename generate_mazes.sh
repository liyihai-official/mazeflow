#! /bin/bash
cp -f param param.save
size=(5 10 15 20 25 30 35 40 45 50 55 60 70 80 100 150 200 250 300 500)
printf "%s\n" "${size[@]}" > param


echo "Default running on $(python --version), at $(which python)."

echo "Calling generate_mazes.py generating Mazes."
for s in "${size[@]}"; do
    echo "Generate Square Mazes with size ${s}"  
    python generate_mazes.py -n 50 -s "$s" -f "$s"
done

