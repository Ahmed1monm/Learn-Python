# Speedup your Python program with concurrency

Link: https://realpython.com/python-concurrency/
Status: Reading
Type: Article

# What is concurrency:

### Threads, Tasks and Process:

All of them can be stopped at point and CPU switches to different one.

-. `[Threading](https://realpython.com/intro-to-python-threading/)`and `asyncio` both run on a single processor and therefore only run one at a time. They just cleverly find ways to take turns to speed up the overall process. Even though they don’t run different trains of thought simultaneously, we still call this concurrency.

### Threading uses ***Pre-emptive Multitasking***

دي بتقطع تنفيذ الثريد في أي نقطة وتنقل على آخر ودي ليها ميزة وعيب 

- الميزة: انك مش محتاج تعمل حاجة ف الكود عشان تنقل على تاسك تاني هو هينقل لوحده
- العيب: انك بتقطع التاسك في أي وقت حتى في السطر الواحد  `x=x+1`

### asyncio uses ***Cooperative Multithreading***

دي بتستنى التاسك يقول هو مستعد يتحول يتنقل امتى عشان البروسيسور يبدأ ينقل

- الميزة: ان التاسك مش هيتقطع ف أي وقت وانت عارف امتى هيحصلك سويتش
- العيب: انك محتاج تحط حاجة ف الكود عشان تعرف البروسيسور انه يسويتش عادي

# What is parallelism?

### Multiprocessing:

بايثون بتعمل بروسيس جديدة بيكون لها الموارد بتاعتها وكل واحدة بتشتغل على منفذ اوامر خاص بيها. فدا معناه انه كل بروسيس قادرة تشتغل على كور خاص بيها ودا معناه ان البروسيسيز كلها هتكون شغالة في نفس الوقت

| Concurrency Type | Switching Decision | Number of Processors |
| --- | --- | --- |
| Pre-emptive multitasking (threading) | The operating system decides when to switch tasks external to Python. |                1 |
| Cooperative multitasking (asyncio) | The tasks decide when to give up control. |                1 |
| Multiprocessing (multiprocessing) | The processes all run at the same time on different processors. |             Many |

# ****When Is Concurrency Useful?****

There is 2 types of problems :

- CPU-bound
- I/O-bound

في أحيان كثيرة بيكون البرنامج بيتعامل مع حاجات ابطأ من البروسيسور لذلك البروسيسور بيكون عطلان زي الفايل سيستم والانترنت مثلا. دي كدا المشكلة التانية 

احيانا بيكون البروسيسور عمل حاجة ف تعليمة معينة ولسه مخلصتش بس في حاجات واقفه فانت بتخليها تشتغل بالتوازي يعني مش هستنى البروسيسور يخلص كل التعليمة مرة واحدة وأبدأ ادخل على اللي بعدها 

| I/O-Bound Process | CPU-Bound Process |
| --- | --- |
| Your program spends most of its time talking to a slow device, like a network connection, a hard drive, or a printer. | You program spends most of its time doing CPU operations. |
| Speeding it up involves overlapping the times spent waiting for these devices. | Speeding it up involves finding ways to do more computations in the same amount of time. |

# ****How to Speed Up an I/O-Bound Program****

## ****Synchronous Version****

```python
import requests
import time

def download_site(url, session):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download_site(url, session)

if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
```

> It is possible to simply use `get()`  from `requests` directly, but creating a `Session` object allows `requests` to do some fancy networking tricks and really speed things up.
> 

> The processing diagram for this program will look much like the I/O-bound diagram in the last section.
> 

> **The big problem here is that it’s relatively slow compared to the other solutions we’ll provide**
> 

![18.399 sec](Speedup%20your%20Python%20program%20with%20concurrency%20fe284ea9c1f64debaf93fa94c2873709/Screenshot_(561).png)

18.399 sec

## Threading version:

```python
import concurrent.futures
import requests
import threading
import time

thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def download_site(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")

def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)

if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    download_all_sites(sites)
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} in {duration} seconds")
```

![3.17 sec](Speedup%20your%20Python%20program%20with%20concurrency%20fe284ea9c1f64debaf93fa94c2873709/Screenshot_(560).png)

3.17 sec

In this version, you’re creating a `ThreadPoolExecutor` 

Thread : غني عن التعريف

Pool : تجميعة او عدد معين 

- This object is going to create a pool of threads, each of which can run concurrently

Executer : باين من الاسم 

- is the part that’s going to control how and when each of the threads in the pool will run. It will execute the request in the pool.

The other interesting change in our example is that each thread needs to create its own `requests.Session()` object

نظام التشغيل هو اللي بيتحكم امتى يقطع الثريد وينتقل لثريد تاني لذلك انت محتاج تحمي الداتا المشتركة بين الثريدز `Protect shared data or Thread safe`

`Requests.session()` isn’t thread safe

### There are several strategies for making data accesses thread-safe depending on what the data is and how you’re using it:

**1 - use thread-safe data structures like `Queue` from Python’s `queue` module.** 

This objects Lock strategy :

- only one thread can access a block of code or a bit of memory at the same time

**2- use here is something called thread local storage.** `thread_local` and `get_session()` :

`local()` is in the `threading` module to specifically solve this problem. It looks a little odd, but you only want to create one of these objects, not one for each thread. The object itself takes care of separating accesses from different threads to different data.

When `get_session()` is called, the `session` it looks up is specific to the particular thread on which it’s running. So each thread will create a single session the first time it calls `get_session()` and then will simply use that session on each subsequent call throughout its lifetime.

---

> في المثال دا احنا مستخدمين 5 ثريدز ممكن تغير الرقم طبعا بس خد بالك انك بعد حد معين من الثريدز الوقت اللي هياخده البرنامج لإنشاء و قتل الثريدز نفسها ممكن يعوض الرقم اللي هو اصلا وفره فانت هتقعد تجرب شوية بقا.
> 

## **The Problems with the `threading` Version :**

1- You have to give some thought to what data is shared between threads

2- Threads can interact in ways that are subtle and hard to detect.

- These interactions can cause race conditions that frequently result in random, intermittent bugs that can be quite difficult to find
    
    ### Race Conditions:
    
    Race conditions happen because the programmer has not sufficiently protected data accesses to prevent threads from interfering with each other. You need to take extra steps when writing threaded code to ensure things are thread-safe.
    
    - نظام التشغيل بيتحكم امتى يغير من ثريد للتاني فممكن في مرة يكون في متغير مشترك بين الثريدز و يجي ثريد بيغير في قيمته وقيمته فعلا اتغيرت بس ملحقش يسجلها في الميموري ويجي نظام التشغيل يروح لثريد تاني في الحالة دي الثريد التاني هيستخدم قيمة خطأ ومننساش ان
        
        `requests.session()` is not thread safe