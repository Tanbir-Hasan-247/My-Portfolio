# portfolio/utils.py
import requests
from bs4 import BeautifulSoup

def get_codeforces_data(username):
    """
    Fetches user data from Codeforces API.
    Makes two API calls: one for user info (rating, pic) and one for submissions (solved count).
    """
    try:
        # First API call for user info
        info_url = f"https://codeforces.com/api/user.info?handles={username}"
        info_response = requests.get(info_url)
        info_response.raise_for_status()
        info_data = info_response.json()

        if info_data['status'] != 'OK':
            return None

        user_info = info_data['result'][0]

        # Second API call for submissions to calculate unique solved problems
        status_url = f"https://codeforces.com/api/user.status?handle={username}"
        status_response = requests.get(status_url)
        status_response.raise_for_status()
        status_data = status_response.json()

        if status_data['status'] != 'OK':
            # Still return basic info if submissions fail
            solved_count = 'N/A'
        else:
            solved_problems = set()
            for submission in status_data['result']:
                if submission.get('verdict') == 'OK':
                    problem = submission['problem']
                    # Create a unique identifier for the problem
                    problem_id = f"{problem.get('contestId')}-{problem.get('index')}"
                    solved_problems.add(problem_id)
            solved_count = len(solved_problems)
        
        return {
            'handle': user_info.get('handle'),
            'rating': user_info.get('rating', 'Unrated'),
            'maxRating': user_info.get('maxRating', 'Unrated'),
            'profile_pic_url': "https:" + user_info.get('titlePhoto'), # Get profile picture
            'solved_count': solved_count, # Add solved count
            'profile_url': f"https://codeforces.com/profile/{username}"
        }
    except requests.RequestException as e:
        print(f"Error fetching Codeforces data: {e}")
    return None


def get_leetcode_data(username):
    """Fetches user data from LeetCode GraphQL API via a third-party service."""
    try:
        url = f"https://leetcode-stats-api.herokuapp.com/{username}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'error':
            print(f"Error fetching LeetCode data: {data.get('message')}")
            return None
            
        return {
            'handle': username,
            'totalSolved': data.get('totalSolved'),
            'acceptanceRate': data.get('acceptanceRate'),
            'profile_pic_url': data.get('avatar'), # Get profile picture
            'profile_url': f"https://leetcode.com/{username}"
        }
    except requests.RequestException as e:
        print(f"Error fetching LeetCode data: {e}")
    return None


def get_codechef_data(username):
    """Scrapes user data from their CodeChef profile page. (Updated for max rating)"""
    try:
        url = f"https://www.codechef.com/users/{username}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        rating = soup.find('div', class_='rating-number').text if soup.find('div', class_='rating-number') else "Unrated"
        
        # Find highest rating from the small text below the main rating
        highest_rating_element = soup.find('div', class_='rating-header')
        max_rating = rating # Default to current rating if max is not found
        if highest_rating_element and 'Highest Rating' in highest_rating_element.text:
            max_rating = highest_rating_element.text.split('Highest Rating')[-1].strip()

        # Find the image element
        profile_pic_element = soup.find('img', class_='user-details-img')
        profile_pic_url = "" 
        if profile_pic_element:
            profile_pic_url = profile_pic_element.get('src', '')

        problems_solved_section = soup.find('section', class_='rating-data-section', id='practice-problems-section')
        solved_count = "0"
        if problems_solved_section:
            count_h3 = problems_solved_section.find('h3')
            if count_h3 and '(' in count_h3.text:
                 solved_count = count_h3.text.split('(')[-1].replace(')', '')
        
        return {
            'handle': username,
            'rating': rating,
            'max_rating': max_rating,
            'solved_count': solved_count,
            'profile_pic_url': profile_pic_url,
            'profile_url': url
        }
    except (requests.RequestException, AttributeError) as e:
        print(f"Error scraping CodeChef data for user '{username}': {e}")
    return None