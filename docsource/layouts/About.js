// Components
import Boot            from '../components/Boot';
import Navbar          from '../components/Navbar';
import SideNav         from '../components/SideNav';
import Footer          from '../components/Footer';
import SearchResults   from '../components/SearchResults';
import EjrbussMarkdown from '../components/EjrbussMarkdown';
import Places          from '../components/Places';
import Profile         from '../components/Profile';

// Libraries
import Pages from '../lib/Pages';
import Vars  from '../Vars';
import { useSearch } from '../lib/hooks';

export default ({ pageName }) => {
    const page      = Pages[pageName];
    const searchCtx = useSearch();
    return (
        <>
            <div id='page'>
            <Boot { ...page } />
                <Navbar 
                    searchCtx={searchCtx}
                    showScrollMarker
                    showSearch
                    leftLinks={<Places {...{ [page.place]: true }} />}
                    rightLinks={<a target='_blank' href={Vars.github} className='p-md subtle-accent'>
                        <i className='fab fa-github fa-lg' />
                    </a>}
                />
                <SideNav />
                <SearchResults searchCtx={searchCtx} />
                <div className='content container grid-md'>
                    <EjrbussMarkdown source=
{`
# Meet Our Team

We are a group of Software, and Electrical, Engineering students from the University of Victoria. With passions for programming, artificial intelligence, and gaming, we came together to deliver an artificial intelligence tool that will enable future generations to share in our love for technology and creating something new.
`}
                    />
                    <Profile src='../static/img/red.png' name='Eric' position='Developer'>
                        <EjrbussMarkdown 
                            source=
{`
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
`}
                        />
                        <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='#' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/red.png' right name='Torrey' position='Developer'>
                        <EjrbussMarkdown 
                            source=
{`
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
`}
                        />
                        <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='#' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/red.png' name='Jon' position='Developer'>
                        <EjrbussMarkdown 
                            source=
{`
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
`}
                        />
                        <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='#' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/red.png' right name='James' position='Developer'>
                        <EjrbussMarkdown 
                            source=
{`
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
`}
                        />
                        <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='#' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/red.png' name='Andrew' position='Developer'>
                        <EjrbussMarkdown 
                            source=
{`
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
`}
                        />
                        <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='#' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <Profile src='../static/img/red.png' right name='Forrest' position='Developer'>
                        <EjrbussMarkdown 
                            source=
{`
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
`}
                        />
                        <a href='#' className='subtle mr-md'><i className='fab fa-linkedin' /></a>
                        <a href='#' className='subtle'><i className='fab fa-github' /></a>
                    </Profile>
                    <EjrbussMarkdown source=
{`
# Acknowledgements
Several people made this project possible and we would like to acknowledge their involvement in Chip-Gr8's development journey, and extend to them our deepest thanks.

## Faculty Supervisor
`}
                    />
                    <Profile src='../static/img/red.png' name='Rich Little' position='Developer'>
                        <EjrbussMarkdown 
                            source=
{`
We chose Rich Little as our faculty supervisor for his background in algorithms and based on our positive experiences with him in CSC 225 and 226 courses. He was responsible for supervising the project during its development cycle and for marking all of the milestones. Thank you to Rich Little for the help he provided along the way.
`}
                        />
                    </Profile>
                    <EjrbussMarkdown source=
{`
We chose Rich Little as our faculty supervisor for his background in algorithms and based on our positive experiences with him in CSC 225 and 226 courses. He was responsible for supervising the project during its development cycle and for marking all of the milestones. Thank you to Rich Little for the help he provided along the way. This is an extra sentence to add padding to this paragraph so that things are aligned better.

## Supporters

#### Dr. Xiaodai Dong
Thank you to Dr. Xiaodai Dong for being the primary instructor this semester.

#### Dr. T. Ilamparithi
Thank you to Dr. Ilamparithi for being the course coordinator this semester.

#### Sai Prakash Reddy Konda
Thank you to the TA for their help with the course.
`}
                    />
                </div>
            </div>
            <Footer />
        </>
    );
};