f = open('.github/workflows/main.yml', 'w')
step = 300
min = 0
max = 18000
number_of_check_download_errors = 20


f.write('''name: parse


on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]


  workflow_dispatch:


jobs:
  preparation:
    runs-on: ubuntu-latest
    steps:     
      - name: Cache preparation
        uses: actions/cache@v2
        with:
          path: ./*
          key: ${{ github.sha }}-preparation
          
      - uses: actions/checkout@v2
        
      - name: setup
        run: |
          pip install requests
          pip install lxml
          pip install beautifulsoup4
      
      - name: rm
        run: |
          rm -rf latest/*

      - name: python
        run: |
          python create_urls.py

      - name: errors
        run: |
          cat latest/urls_errors.txt
          

  errors_check_1:
    runs-on: ubuntu-latest
    needs: preparation
    steps:
      - name: Cache errors_check_1
        uses: actions/cache@v2
        with:
          path: ./*
          key: ${{ github.sha }}-errors_check_1

      - name: Cache preparation
        uses: actions/cache@v2
        with:
          path: ./*
          key: ${{ github.sha }}-preparation
        
      - name: setup
        run: |
          pip install requests
          pip install lxml
          pip install beautifulsoup4

      - name: python
        run: |
          python urls_errors_check.py

      - name: errors
        run: |
          cat latest/urls_errors.txt
                    

  errors_check_2:
    runs-on: ubuntu-latest
    needs: errors_check_1
    steps:
      - name: Cache errors_check_2
        uses: actions/cache@v2
        with:
          path: ./*
          key: ${{ github.sha }}-errors_check_2

      - name: Cache errors_check_1
        uses: actions/cache@v2
        with:
          path: ./*
          key: ${{ github.sha }}-errors_check_1

      - name: setup
        run: |
          pip install requests
          pip install lxml
          pip install beautifulsoup4

      - name: python
        run: |
          python urls_errors_check.py

      - name: errors
        run: |
          cat latest/urls_errors.txt
            
      # - name: tree
      #   run: |
      #     sudo apt install -y tree
      #     tree
      
''')


for i in range(min, max, step):
    f.write(f'''  download_{i}:
    runs-on: ubuntu-latest
    needs: errors_check_2
    steps:
      - name: Cache 
        uses: actions/cache@v2
        with:
          path: latest/pages/{i}/*
          key: ${{{{ github.sha }}}}-download_{i}

      - name: Cache 
        uses: actions/cache@v2
        with:
          path: ./*
          key: ${{{{ github.sha }}}}-errors_check_2
                    
      - name: setup
        run: |
          pip install BeautifulSoup4
          pip install requests
          pip install eventlet

      - name: download pages
        run: |
          python3 download.py {step} {i}
            
''')


f.write('''  assembling:
    runs-on: ubuntu-latest
    needs: [''')
for i in range(min, max, step):
    f.write(f'''download_{i}, ''')
f.write(''']
    steps:
      - uses: actions/checkout@v2
      
      - name: Cache assembled
        uses: actions/cache@v2
        with:
          path: latest/*
          key: ${{ github.sha }}-assembled
''')
for i in range(min, max, step):
    f.write(f'''      
      - name: Cache download_{i}
        uses: actions/cache@v2
        with:
          path: latest/pages/{i}/*
          key: ${{{{ github.sha }}}}-download_{i}
''')


f.write(f'''
  download_errors_check_1:
    runs-on: ubuntu-latest
    needs: assembling
    steps:
      - uses: actions/checkout@v2
      
      - name: Cache download_errors_check_1
        uses: actions/cache@v2
        with:
          path: latest/*
          key: ${{{{ github.sha }}}}-download_errors_check_1
          
      - name: Cache assembled
        uses: actions/cache@v2
        with:
          path: latest/*
          key: ${{{{ github.sha }}}}-assembled

      - name: setup
        run: |
          pip install BeautifulSoup4
          pip install requests

      - name: download pages
        run: |
          python3 download_errors_check.py {step} 
    
      - name: errors
        run: |
          cat latest/pages/download_errors.txt || echo No errors

''')
for i in range(2, number_of_check_download_errors + 1, 1):
    f.write(f'''
  download_errors_check_{i}:
    runs-on: ubuntu-latest
    needs: download_errors_check_{i - 1}
    steps:
      - uses: actions/checkout@v2
      
      - name: Cache download_errors_check_{i}
        uses: actions/cache@v2
        with:
          path: latest/*
          key: ${{{{ github.sha }}}}-download_errors_check_{i}

      - name: Cache download_errors_check_{i - 1}
        uses: actions/cache@v2
        with:
          path: latest/*
          key: ${{{{ github.sha }}}}-download_errors_check_{i - 1}

      - name: setup
        run: |
          pip install BeautifulSoup4
          pip install requests

      - name: download pages
        run: |
          python3 download_errors_check.py {step} 
    
      - name: errors
        run: |
          cat latest/pages/download_errors.txt || echo No errors
''')

f.write(f'''
  parse:
    runs-on: ubuntu-latest
    needs: download_errors_check_{number_of_check_download_errors}
    steps:
      - uses: actions/checkout@v2
      
      - name: Cache 
        uses: actions/cache@v2
        id: download_errors_check_{number_of_check_download_errors}
        with:
          path: latest/*
          key: ${{{{ github.sha }}}}-download_errors_check_{number_of_check_download_errors}
          
      - name: setup 
        run: | 
          pip install pandas
          pip install lxml
          pip install BeautifulSoup4
      
      - name: tree
        run: |
          sudo apt install -y tree
          tree
          
      - name: python
        run: |
          python parse.py || echo error
          
      # - name: rm
      #   run: |
      #     rm -rf latest/*
          
      - name: tree
        run: |
          tree
              
      - name: setup git
        env:
          GIT_EMAIL: ${{{{ secrets.GIT_EMAIL }}}}
          GIT_NAME: ${{{{ secrets.GIT_NAME }}}}
        run: |
          git config --global user.email $GIT_EMAIL
          git config --global user.name $GIT_NAME
          curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
          sudo apt-get install -y git-lfs
          git lfs install

      - name: git add 
        run: |
          date=$(date '+%Y-%m-%d_%H:%M:%S')
          git add -A
          git commit -m $date

      - name: git push
        run: |
          git push

''')
