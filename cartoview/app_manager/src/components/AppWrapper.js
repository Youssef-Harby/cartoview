import React, { Fragment, useState, useContext } from 'react';
import Modal from './Modal';
import classes from '../css/AppWrapper.module.css';
import AppsContext from "../store/apps-context";
import { csrftoken } from '../../static/app_manager/js/csrf_token';

const AppWrapper = (props) => {
    const REST_URL = 'http://localhost:8000/apps/rest/app_manager/';
    const appstore_id = 1;
    const appsContext = useContext(AppsContext);

    // extract props
    const { app, buttonStatus, toggleButtonStatus, toggleRestartServer } = props;

    // app status
    const [isActive, setIsActive] = useState(app.active);

    const [showUninstallingModal, setShowUninstallingModal] = useState(false);
    const [showInstallingModal, setShowInstallingModal] = useState(false);

    const [uninstalling, setUninstalling] = useState(false);
    const [installing, setInstalling] = useState(false);

    // toggle install modal (show or hide)
    const toggleUninstallingModal = () => {
        setShowUninstallingModal(prevState => {return !prevState});
    }

    // toggle uninstalling modal (show or hide)
    const toggleInstallingModal = () => {
        setShowInstallingModal(prevState => {return !prevState})
    }

    // toggle active state of an app (active or suspended)
    const toggleActivate = () => {
        isActive ? suspendApp() : activateApp();
        setIsActive(prevState => { return !prevState });
    }

    // toggle uninstalling state (true or false)
    const toggleUninstalling = () => {
        setUninstalling(prevState => { return !prevState });
    }

    // toggle installing state (true or false)
    const toggleInstalling = () => {
        setInstalling( prevState => {
            return !prevState;
        })
    }

    // suspend active app
    const suspendApp = () => {
        toggleButtonStatus();
        fetch(REST_URL + `app/${app.store_id}/suspend/`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },

        })
            .then(response => {
                if(!response.ok){
                    throw new Error('Error suspending App ' + app.name);
                }
                toggleButtonStatus();
                return response.json()
            })
            .then(data => {
                if(data){
                    console.log(data);
                }
                else{
                    throw new Error('Error suspending App ' + app.name);
                }
            })
            .catch(error => {
                toggleButtonStatus();
                appsContext.setError(error.message);
            })
    }

    // activate suspended app
    const activateApp = () => {
        toggleButtonStatus();
        fetch(REST_URL + `app/${app.store_id}/activate/`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then(response => {
                if(!response.ok){
                    throw new Error('Error Activating App ' + app.name);
                }
                toggleButtonStatus();
                return response.json()
            })
            .then(data => {
                if(data){
                    console.log(data);
                }
                else{
                    throw new Error('Error Activating App ' + app.name);
                }
            })
            .catch(error => {
                toggleButtonStatus();
                appsContext.setError(error.message);
            });
    }

    // install app
    // Url = 'http://localhost:8000/api/app/install/'
    // payload = {apps: [{'app_name', 'version', 'store_id'}], restart: false}
    const installApp = () => {
        toggleButtonStatus();
        toggleInstalling();
        if(showInstallingModal){
            toggleInstallingModal();
        }
        let apps = [];

        // push the main app to the payload
        apps.push({"app_name": app.name, "version": app.latest_version.version, "store_id": appstore_id});

        console.log('apps', apps);
        fetch('../../api/app/install/', {
            method: 'POST',
            headers: {
                "Accept": 'application/json',
                'Content-Type': 'application/json',
                "X_CSRFToken": csrftoken
            },
            body: JSON.stringify({
                apps: apps,
                restart: false,
            })
        })
            .then(response => {
                if(!response.ok){
                    throw new Error('Error Installing app ' + app.name);
                }
                toggleButtonStatus();
                toggleInstalling();
                toggleRestartServer();
                // scroll to the top of the page to restart server
                window.scroll({top: 0, left: 0, behavior: 'smooth' });
                return response.json();
            })
            .then(data => {
                if(data) {
                    console.log(data);
                }
                else{
                    throw new Error('Error Installing app ' + app.name);
                }
            })
            .catch(error => {
                toggleButtonStatus();
                toggleInstalling();
                appsContext.setError(error.message);
            });
    }

    // uninstall app
    // url = 'http://localhost:8000/apps/uninstall/:store_id/:app_name'
    const uninstallApp = (app_name, store_id) => {
        toggleUninstalling();
        toggleButtonStatus();
        fetch(`../uninstall/${store_id}/${app_name}/`, {
            method: 'POST',
            headers: {
                "Accept": 'application/json',
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
        })
            .then(response => {
                if(!response.ok){
                    throw new Error('Error Uninstalling app ' + app.name);
                }
                toggleButtonStatus();
                toggleUninstalling();
                return response.json()
            })
            .then(data => {
                if(data) {
                    console.log(data);
                    // Reload page after uninstalling app
                    window.location.reload();
                }
                else{
                    throw new Error('Error Uninstalling app ' + app.name);
                }
            })
            .catch(error => {
                toggleUninstalling();
                toggleButtonStatus();
                appsContext.setError(error.message);
            })
        ;

    }

    // handle Install button
    const handleInstall = () => {
        // get dependencies of the app to be installed also
        let dependencies = app.latest_version.dependencies;

        //if this app depend on another apps need to be installed first
        if(Object.keys(dependencies).length){
            toggleInstallingModal();
        }
        else{
         // install main app here
          installApp();
        }
    }

    // handle uninstall button
    const handleUninstall = () => {
        toggleUninstallingModal();
        // get dependencies of the app to be uninstalled also
        let dependencies = app.latest_version.dependencies;
        dependencies = Object.keys(dependencies);

        // uninstall app with dependencies if exist
        if (dependencies.length > 0) {
            toggleUninstalling();
            toggleButtonStatus();
            // first uninstall the main app and after it's request is done
            // uninstall it's dependencies in sync
             fetch(`../uninstall/${appstore_id}/${app.name}/`, {
                    method: 'POST',
                    headers: {
                        "Accept": 'application/json',
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrftoken
                    },
                })
                 .then(response => {
                     if(!response){
                         throw new Error('Error Uninstalling app ' + app.name);
                     }
                     return response.json();
                 })
                 .then(data => {
                     console.log(data);

                     // here start uninstalling app dependencies
                     dependencies.forEach(appName => {
                         console.log('uninstalling', appName);
                          fetch(`../uninstall/${appstore_id}/${appName}/`, {
                            method: 'POST',
                            headers: {
                                "Accept": 'application/json',
                                "Content-Type": "application/json",
                                "X-CSRFToken": csrftoken
                            },
                            })
                        .then(response => {
                            if(!response.ok){
                                throw new Error('Error Uninstalling app ' + appName);
                            }
                            return response.json();
                        })
                        .then(data => {
                             // after uninstalling dependencies
                            toggleUninstalling();
                            toggleButtonStatus();
                            console.log(data);
                            // Reload page after finish uninstalling
                            window.location.reload();
                        }).catch(error => {
                            // catch dependencies errors
                            toggleUninstalling();
                            toggleButtonStatus();
                            appsContext.setError(error.message);
                          })
                     })
                     .catch(error => {
                        toggleUninstalling();
                        toggleButtonStatus();
                        appsContext.setError(error.message);
                      })
                     ;
                 })
        }
        else{
            //  uninstall single app (no dependencies)
            uninstallApp(app.name, appstore_id);
        }
    }

    // available app actions content
    const available = <>{ installing  ? <button type='button' className='btn btn-default' onClick={handleInstall} disabled={buttonStatus}>
        <i className="fa fa-circle-o-notch fa-spin"></i>
        Installing
    </button> : <button type='button' className='btn btn-default' onClick={handleInstall} disabled={buttonStatus}>
        <span className="glyphicon glyphicon-download-alt" aria-hidden="true"></span>
        Install
    </button>}</>;



    // installed apps actions content
    const installed = <>{uninstalling ? <button type='button' className='btn btn-danger' disabled={buttonStatus}>
        <i className="fa fa-circle-o-notch fa-spin"></i>Uninstall
    </button> :
        <button type='button' className='btn btn-danger' disabled={buttonStatus} onClick={toggleUninstallingModal}>
            <span className="glyphicon glyphicon-remove" aria-hidden="true"></span>
            Uninstall</button>

    }
        {isActive ?
            <button type='button' className='btn btn-warning' onClick={toggleActivate} disabled={buttonStatus}>
                <span className="glyphicon glyphicon-pause" aria-hidden="true"></span>
                Suspend</button> :
            <button type='button' className='btn-success' onClick={toggleActivate} disabled={buttonStatus}>
                <span className="glyphicon glyphicon-play" aria-hidden="true"></span>
                Activate</button>
        }</>;

    return (
        <Fragment>
            {showUninstallingModal && <Modal app={app} handleToggle={toggleUninstallingModal} handleConfirm={handleUninstall} flag={'uninstalling'}/>}
            {showInstallingModal && <Modal app={app} handleToggle={toggleInstallingModal} handleConfirm={installApp} flag={'installing'}/>}
            <div className={`${classes.card} col-md-6 col-sm-12 col-xs-12`}>
                <div className={classes['app-description']}>
                    <img src={app.latest_version.logo} />
                    <h4>{app.title}</h4>
                    {app.description.length > 150 ? <p>{app.description.slice(0, 100) + '...'}</p> :
                        <p>{app.description}</p>
                    }

                </div>

                <div className={classes['app-actions']}>
                    {app.installed ? installed : available}
                </div>

                <div className={classes['app-info']}>
                    <ul>
                        <li><b>Rating: </b> <span> {app.stars} / 5</span></li>
                        <li><b>Latest version: </b> <span>V {app.latest_version.version}</span></li>
                        <li><b>Installed Version:</b> <span>V {app.installed ? app.latest_version.version : ''}</span></li>
                        <li><b>Installation:</b>{app.downloads}</li>
                        <li><b>By: </b>{app.author}</li>
                    </ul>
                </div>
            </div>
        </Fragment>
    )
};

export default AppWrapper;


